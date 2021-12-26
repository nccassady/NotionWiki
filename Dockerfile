FROM public.ecr.aws/lambda/python:3.9

RUN yum install libcurl-devel openssl-devel python39-devel gcc -y

ENV PYCURL_SSL_LIBRARY=openssl

# Install the function's dependencies using file requirements.txt
# from your project folder.
COPY requirements.txt  .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Copy function code
ADD src ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.lambda_handler" ]