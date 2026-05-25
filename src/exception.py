# Excpetion handling purpose 
import sys # sys helps in interacting the python code with python interpreter 
import logging



def error_message_detail (error,error_detail:sys):
    _,_,exc_tb=error_detail.exc_info()   # provide the info on which file and on which part of the line the error has occured
    file_name=exc_tb.tb_frame.f_code.co_filename
    error_messages="Error ocuured in python script name [{0}] line number [{1}] error messages[{2}]".format(
     file_name,exc_tb.tb_lineno,str(error)

     )
    return error_messages

class CustomeException(Exception):
    def __init__(self,error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_message=error_message_detail(error_message,error_detail=error_detail)

    def __str__(self):
        return self.error_message
    
if __name__=="__main__":
    try:
        a=1/0
    except Exception as e:
        logging.info("Divide by zero error")
        raise CustomeException(e,sys)