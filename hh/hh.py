from .config import Config
import requests

from .schemas import (
    MeHHSchema,
    VacancySearchParamsHHSchema,
    ShortVacancyListHHSchema,
    VacancyHHSchema,
    ShortVacancyHHSchema
)


def get_hh_me(conf=Config()) -> MeHHSchema:
    response = requests.get(f"{conf.base_url}/me", headers=conf.hh_headers)
    if response.status_code != 200:
        raise ValueError(response.reason)
    json_dict = response.json()
    return MeHHSchema.parse_obj(json_dict)


def get_hh_vacancies_obj(params: VacancySearchParamsHHSchema, conf=Config()) -> ShortVacancyListHHSchema:
    params_str = params.get_params()
    response = requests.get(f"{conf.base_url}/vacancies{params_str}", headers=conf.hh_headers)
    if response.status_code != 200:
        raise ValueError(response.reason)
    json_dict = response.json()
    obj = ShortVacancyListHHSchema.parse_obj(json_dict)
    return obj


def get_hh_short_vacancies(params: VacancySearchParamsHHSchema, limit=20, conf=Config()) -> list[ShortVacancyHHSchema]:
    items = get_hh_vacancies_obj(params=params, conf=conf).items
    # TODO: в зависимости от лимита доп запросы делать
    return items


def get_hh_vacancy(vacancy_id: str, conf=Config()) -> VacancyHHSchema:
    response = requests.get(f"{conf.base_url}/vacancies/{vacancy_id}", headers=conf.hh_headers)
    if response.status_code != 200:
        raise ValueError(response.reason)
    json_dict = response.json()
    return VacancyHHSchema.parse_obj(json_dict)
