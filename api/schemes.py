from pydantic import AliasChoices, AliasPath
from pydantic.main import create_model
from pydantic.fields import FieldInfo


def erate_fieldinfo_generator(target_unit):
    """
    Генерирует параметры поля `target_unit` с заданным названием 
    `target_unit` = `ИМЯ_ДЕНЕЖНОЙ_ЕДИНИЦЫ`
    и где его нужно искать в структуре json внешнего api
    """
    return FieldInfo(
        annotation=float, 
        required=True, 
        alias_priority=2, 
        validation_alias=AliasChoices(
            target_unit, 
            AliasPath(
                'conversion_rates', target_unit
            )
        )
    )

def erate_generator(target_unit):
    """
    Задаёт модель структуры данных 
    текущего курса доллара к денежной единице 
    `target_unit`
    """
    return create_model(
        "ExchangeRate",
        **{
            target_unit: (float, erate_fieldinfo_generator(target_unit))
        }
    )

def erate_datacls_generator(target_unit):
    """
    Генерирует модель данных курса доллара по 
    отношению целевой денежной единице `target_unit`
    """
    datatype = erate_generator(target_unit)
    return create_model(
        "CurrentExchangeRateData",
        **{
            "data": (datatype, FieldInfo(
                annotation=datatype,
                default=None,
                validate_default=False
            ))
        }
    )
