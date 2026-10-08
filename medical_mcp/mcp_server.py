from fastmcp import FastMCP
from database import get_doctor , get_patient
from src.exception import CustomException
from src.logger import get_logger
logger = get_logger(__name__)

mcp = FastMCP("MEDICO CLINIC")


# TOOL TO GET DOCTOS DETAILS:::
@mcp.tool()
def doctor_details(name:str):
    doctor = get_doctor(name)
    if not doctor:
        return {
            "success": False,
            "message": f"Doctor {name} not found."
        }
    return {
        "success": True,
        "Doctor": {
            'id ': doctor[0],
            'name ': doctor[1],
            'specializtion ': doctor[2],
            'timing' : doctor[3]
        }
    }


# TOOL TO GET PATIENTS DETAILS:::
@mcp.tool()
def patient_details(patient_id: int):
    patient = get_patient(patient_id)
    if not patient:
        return {
            "success": False,
            "message": f"Patient {patient_id} not found."
        }
    return {
        "success ": True,
        "Patient" : {
            'id ': patient[0],
            'name ': patient[1],
            'age ': patient[2],
            'city ': patient[3],
            'blood-group ': patient[4]
        }
    }


# FOR LOGS::::
print(logger.info("TOOLS SETUP FOR MCP MEDICAL SERVER"))


# TO RUN MCP SERVER:::
if __name__=="__main__":
    mcp.run(transport="http" , host="0.0.0.0" , port=8001)