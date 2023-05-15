#De aqui se agarra la imagen original para la creacion de Lambda System
FROM public.ecr.aws/lambda/python:3.9


# Install the function's dependencies using file requirements.txt
# from your project folder.

COPY requirements.txt  .

RUN yum update -y && \
  yum install -y git && \
  yum install -y curl && \
  rm -Rf /var/cache/yum

RUN  pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"
#Se le hace upgrade a urllib3 por problemas de compatibilidad con BOTO3 y LANGCHAIN
RUN pip install --upgrade urllib3 --target "${LAMBDA_TASK_ROOT}"
# Copy function code
COPY app.py ${LAMBDA_TASK_ROOT}
COPY kendra_results.py ${LAMBDA_TASK_ROOT}
COPY kendra_index_retriever.py ${LAMBDA_TASK_ROOT}


# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.lambda_handler" ] 

