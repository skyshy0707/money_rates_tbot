from fastapi import APIRouter, Depends, Path, status

from . import load_data, schemes

async def lastest_rate_model_response(target_unit: str=Path(...)):
    return schemes.erate_datacls_generator(target_unit=target_unit)


class Router:

    def __init__(self):
        self.router = APIRouter()
        self.setup_routes()

    def setup_routes(self):
        
        @self.router.get(
            "/latest/{target_unit}", 
            description="Текущий курс доллара к какой-то валюте",
            status_code=status.HTTP_200_OK
        )
        async def get_lastest_rate(response_model=Depends(lastest_rate_model_response)):
            return load_data.get_rate_api_data(response_model)
        

weatherapi = Router()