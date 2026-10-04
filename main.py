import os 
import sys
import uvicorn
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.exception import CustomException
from src.logger import get_logger
logger = get_logger(__name__)
from src.pipeline.predict_pipeline import CustomData, PredictPipeline
app= FastAPI(title="Covid Prediction Clinic")

from nlp_pretrained.ner_tagger import(get_pos_tags , extract_entities)
from nlp_pretrained.embedding import(most_similar_words)
from nlp_pretrained.sentiment_analyzer import analyze_sentiment

# MOunting the CSS file
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set the Template Folder
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request:Request):
    logger.info("Home page accessed...")
    return templates.TemplateResponse(request, "index.html")


@app.get("/predict", response_class=HTMLResponse)
async def predict_form(request:Request):
    logger.info("Predict form page accessed")
    return templates.TemplateResponse(request, "predict.html", {"result": None})

@app.post("/predict", response_class=HTMLResponse)
async def predict_resuult(
    request: Request,
    age:int = Form(...),
    gender:str = Form(...),
    fever: float = Form(...),
    cough: str = Form(...),
    city: str = Form(...)
):
    try:
        logger.info(f"Prediction request recieved: age{age}, gender{gender}, fever{fever}, cough{cough}, city{city}")
        custom_data = CustomData(age=age, gender=gender, fever=fever, cough=cough, city=city)
        data_df = custom_data.get_data_as_dataframe()
        predict_pipeline = PredictPipeline()
        result, probability = predict_pipeline.predict(data_df)
        return templates.TemplateResponse(
            request,
            "predict.html",
            {
                "result": result,
                "probability": probability,
                "form_data": {
                    "age": age,
                    "gender": gender,
                    "fever": fever,
                    "cough": cough,
                    "city": city
                }
            }

        )
    except Exception as e:
        raise CustomException(e, sys)


@app.get("/health")
async def health_check():
    logger.info("Monitoring alert...")
    return {"status":"ok"}


@app.get("/pretrained-nlp" , response_class=HTMLResponse)
async def pretrained_nlp_form(request: Request):
    return templates.TemplateResponse(request,
                                      "pretrained_nlp.html",
                                      {
                                          "resultt": None,
                                          "form_data": {
                                              "query":""
                                          },
                                          "error": None
                                          
                                      })

@app.post("/pretrained-nlp" , response_class=HTMLResponse)
async def pretrained_nlp_analysis(
    request: Request,
    query: str= Form(...)
):
    try:
        # text clean
        query = query.strip()
        if not query:
            return templates.TemplateResponse(
                request,
                "pretrained_nlp.html",
                {
                    "result": None,
                    "form_data": {
                        "query": ""
                    },
                    "error": "Please enter some text."
                }
            )

        # POS TAGGING
        pos_tags = get_pos_tags(query)

        #  NER
        entities = extract_entities(query)

        # SENTIMENT ANALYSIS
        sentiment = analyze_sentiment(query)

        # WoRD EMBEDDINGS
        similar_words = []
        words = query.split()
        first_word = words[0].lower()
        if words:
            try:
                similar_words = most_similar_words(first_word, topn= 5)
            except Exception as e:
                logger.warning(f"Glove Similarity failed for: " , {first_word}, "and error is: ", {e})
                similar_words= []
        # final result 
        result = {
            "query": query,
            "pos_tagss": pos_tags,
            "entities": entities,
            "similar_words": similar_words,
            "sentiment": sentiment
        }

        # render result
        return templates.TemplateResponse(
            request,
            "pretrained_nlp.html",
            {
                "result": result,
                "Form_data": {
                    "query": query
                },
                "error": None
            }
        )
                 
    except Exception as e:
        logger.info("Error occured in pretrained nlp analysis")
        return templates.TemplateResponse(
            request,
            "pretrained_nlp.html",
            {
                "result": None,
                "Form_data": {
                    "query": query,
                },
                "error": str(e)
            }
        )
        

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", post=8000, reload=True)