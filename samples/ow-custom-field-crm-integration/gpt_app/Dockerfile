FROM public.ecr.aws/lambda/python:3.10-x86_64

COPY requirements.txt ${LAMBDA_TASK_ROOT}/
COPY ./handler.py ${LAMBDA_TASK_ROOT}/
COPY ./func_items.py ${LAMBDA_TASK_ROOT}/
COPY ./__init__.py ${LAMBDA_TASK_ROOT}/

RUN pip install -U --no-cache-dir -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

CMD ["handler.lambda_handler"]