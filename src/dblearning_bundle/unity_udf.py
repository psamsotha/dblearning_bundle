import inspect

from typing import Callable
from pyspark.sql import SparkSession

def squared(v: int) -> int:
  return v * v

tmp = """
CREATE OR REPLACE FUNCTION main.default.{udf_declaration}
RETURNS {return_type}
LANGUAGE PYTHON
AS $$
  {udf_body}
$$
"""

type_map = {
  'int': 'INTEGER',
  'str': 'STRING',
  'typing.Long': 'BIGINT'
}

function_code = inspect.getsource(squared)
function_declaration, function_body = function_code.split('\n', maxsplit=1)

second_declaration = function_declaration.replace('def', '').split('->')[0].strip()
for ptype, dbtype in type_map.items():
  second_declaration = second_declaration.replace(ptype, dbtype)
second_declaration = second_declaration.replace(':', '')

return_type = function_declaration.split()[-1].replace(':', '').strip()
return_type = type_map[return_type]

print(f'function_declaration: {function_declaration}')
print(f'function_body: {function_body}')
print(f'return_type: {return_type}')
print(f'second_declaration: {second_declaration}')

sql_query = tmp.format(
  function_declaration=second_declaration,
  return_type=return_type,
  function_body=function_body
)
print('sql_query')
print(sql_query)

def create_unity_udf(spark: SparkSession, func: Callable) -> None:
  func_code = inspect.getsource(func)
  func_declaration, function_body = func_code.split('\n', maxsplit=1)

  udf_declaration = func_declaration.replace('def', '').split('->')[0].strip()
  for ptype, dbtype in type_map.items():
    udf_declaration = udf_declaration.replace(ptype, dbtype)
  udf_declaration = udf_declaration.replace(':', '')

  return_type = func_declaration.split()[-1].replace(':', '').strip()
  return_type = type_map[return_type]

  create_udf_query = tmp.format(
    udf_declaration=udf_declaration,
    return_type=return_type,
    udf_body=function_body
  )
  
  spark.sql(create_udf_query)
