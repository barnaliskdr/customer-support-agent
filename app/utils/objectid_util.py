
# from bson import ObjectId
# from pydantic import GetJsonSchemaHandler
# from pydantic.json_schema import JsonSchemaValue

# class PyObjectId(ObjectId):
#     @classmethod
#     def __get_pydantic_core_schema__(cls, _source_type, _handler):
#         from pydantic_core import core_schema
#         return core_schema.no_info_after_validator_function(cls.validate, core_schema.str_schema())

#     @classmethod
#     def validate(cls, v):
#         if isinstance(v, ObjectId):
#             return v
#         if not ObjectId.is_valid(v):
#             raise ValueError("Invalid ObjectId")
#         return ObjectId(v)

#     @classmethod
#     def __get_pydantic_json_schema__(
#         cls, schema: JsonSchemaValue, handler: GetJsonSchemaHandler
#     ) -> JsonSchemaValue:
#         schema = handler(schema)
#         schema.update(type="string")
#         return schema


from bson import ObjectId
from pydantic import GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue


class PyObjectId(ObjectId):
    """Custom type to integrate MongoDB ObjectId with Pydantic v2"""

    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handler):
        from pydantic_core import core_schema

        # Accept either a string or ObjectId, and convert to ObjectId
        def validate(value):
            if isinstance(value, ObjectId):
                return value
            if ObjectId.is_valid(value):
                return ObjectId(value)
            raise ValueError("Invalid ObjectId")

        return core_schema.no_info_after_validator_function(validate, core_schema.union_schema([
            core_schema.str_schema(),
            core_schema.is_instance_schema(ObjectId),
        ]))

    @classmethod
    def __get_pydantic_json_schema__(
        cls, schema: JsonSchemaValue, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        schema = handler(schema)
        schema.update(type="string")  # For OpenAPI docs
        return schema
