from typing import Optional, Union
from pydantic import BaseModel, Field, HttpUrl, conint
from libs import HTML
from datetime import datetime, date


class MeHHSchema(BaseModel):
    auth_type: str
    is_applicant: bool
    is_employer: bool
    is_admin: bool
    is_application: bool


class IdNameHHSchema(BaseModel):
    id: str = Field(description="Идентификатор")
    name: str = Field(description="Название")


class AreaHHSchema(IdNameHHSchema):
    url: HttpUrl = Field(description="Url получения информации о регионе")


class InsiderInterviewHHSchema(BaseModel):
    id: str = Field(description="идентификатор интервью")
    url: HttpUrl = Field(description="адрес страницы, содержащей интервью")
    title: Optional[HttpUrl] = Field(description="заголовок интервью")


class SalaryHHSchema(BaseModel):
    from_: Optional[int] = Field(alias="from", description="Нижняя граница вилки оклада")
    to_: Optional[int] = Field(alias="to", description="Верняя граница вилки оклада")
    gross: Optional[bool] = Field(description="Признак того что оклад указан до вычета налогов. В случае если не указано - null.")
    currency: str = Field(description="Идентификатор валюты оклада (справочник currency). https://github.com/hhru/api/blob/master/docs/dictionaries.md")


class MetroStationsHHSchema(BaseModel):
    station_id: str = Field(description="Идентификатор станции метро", example="6.8")
    station_name: str = Field(description="Название станции метро", example="Алексеевская")
    line_id: str = Field(description="Идентификатор линии метро, на которой находится станция", example="6")
    line_name: str = Field(description="Название линии метро, на которой находится станция", example="Калужско-Рижская")
    lat: Optional[float] = Field(description="Географическая широта", example=55.807794)
    lng: Optional[float] = Field(description="Географическая долгота", example=37.638699)


class AddressHHSchema(BaseModel):
    city: Optional[str] = Field(description="Город")
    street: Optional[str] = Field(description="Улица")
    building: Optional[str] = Field(description="Номер дома")
    description: Optional[str] = Field(description="Дополнительная информация об адресе", example="на проходной потребуется паспорт")
    lat: Optional[float] = Field(description="Географическая широта", example=55.807794)
    lng: Optional[float] = Field(description="Географическая долгота", example=37.638699)
    metro_stations: list[MetroStationsHHSchema] = Field(description="Список станций метро, может быть пустым")


class KeySkillHHSchema(BaseModel):
    name: str = Field(description="название ключевого навыка")


class TestHHSchema(BaseModel):
    required: bool = Field(description="Обязательно ли заполнение теста для отклика")


class SpecializationHHSchema(IdNameHHSchema):
    profarea_id: str = Field(description="Идентификатор профессиональной области, в которую входит специализация", example="1")
    profarea_name: str = Field(description="Название профессиональной области, в которую входит специализация")


class VacancyEmployerHHSchema(BaseModel):
    # TODO: EmployerHHSchema не описана https://github.com/hhru/api/blob/master/docs/employers.md#item
    blacklisted: Optional[bool] = Field(description="Добавлены ли все вакансии работодателя в список скрытых")


class PhoneHHSchema(BaseModel):
    country: str = Field(description="Код страны")
    city: str = Field(description="Код города")
    number: str = Field(description="Номер телефона")
    comment: Optional[str] = Field(description="Комментарий")


class ContactsHHSchema(BaseModel):
    name: Optional[str] = Field(description="Имя контактного лица")
    email: Optional[str] = Field(description="Email контактного лица")
    phones: list[PhoneHHSchema] = Field(description="Список телефонов контактного лица. Может быть пустым.")


class LogoUrlsHHSchema(BaseModel):
    original: HttpUrl
    image_240: HttpUrl = Field(alias="240")
    image_90: HttpUrl = Field(alias="90")


class ShortEmployerHHSchema(BaseModel):
    id: str = Field(description="идентификатор работодателя")
    name: str = Field(description="название работодателя")
    url: Optional[HttpUrl] = Field(description="url для получения полного описания работодателя")
    alternate_url: HttpUrl = Field(description="ссылка на описание работодателя на сайте")
    vacancies_url: HttpUrl = Field(description="url для получения поисковой выдачи с вакансиями данной компании")
    open_vacancies: Optional[int] = Field(description="оличество открытых вакансий у работодателя")
    logo_urls: Optional[LogoUrlsHHSchema] = Field(description="логотипы компании")


class ShortVacancyHHSchema(BaseModel):
    id: str = Field(description="Идентификатор вакансии")
    premium: bool = Field(description="Является ли данная вакансия премиум-вакансией")
    has_test: bool = Field(description="Информация о наличии прикрепленного тестового задании к вакансии. В случае присутствия теста - true.")
    response_url: Optional[str] = Field(description="На вакансии с типом direct нельзя откликнуться на сайте hh.ru, у этих вакансий в ключе response_url выдаётся URL внешнего сайта (чаще всего это сайт работодателя с формой отклика).")
    address: Optional[AddressHHSchema] = Field(description="Адрес вакансии")
    alternate_url: str = Field(description="Ссылка на представление вакансии на сайте")
    apply_alternate_url: str = Field(description="Ссылка на отклик на вакансию на сайте")
    department: Optional[IdNameHHSchema] = Field(description="Департамент, от имени которого размещается вакансия (если данная возможность доступна для компании). Работодатели могут запросить справочник департаментов.")
    salary: Optional[SalaryHHSchema] = Field(description="Признак того что оклад указан до вычета налогов. В случае если не указано - null.")
    name: str = Field(description="Название вакансии")
    insider_interview: Optional[InsiderInterviewHHSchema] = Field(description="Интервью о жизни в компании")
    area: AreaHHSchema = Field(description="Регион размещения вакансии")
    url: Optional[HttpUrl]
    published_at: datetime = Field(description="Дата и время публикации вакансии")
    relations: Optional[list[dict]]
    employer: Optional[ShortEmployerHHSchema] = Field(description="Короткое представление работодателя. Описание полей смотрите в информации о работодателе. Может не прийти в случае, если вакансия анонимная")
    response_letter_required: bool = Field(description="Обязательно ли заполнять сообщение при отклике на вакансию")
    type: IdNameHHSchema = Field(description="Тип вакансии. Элемент справочника vacancy_type.")
    archived: bool = Field(description="Находится ли данная вакансия в архиве")
    working_days: list[IdNameHHSchema] = Field(description="Рабочие дни. Элемент справочника working_days")
    working_time_intervals: list[IdNameHHSchema] = Field(description="Временные интервалы работы. Элемент справочника working_time_intervals")
    working_time_modes: list[IdNameHHSchema] = Field(description="Режимы времени работы. Элемент справочника working_time_modes")
    accept_temporary: Optional[bool] = Field(description="Указание, что вакансия доступна для соискателей с временным трудоустройством")
    sort_point_distance: Optional[int] = Field(description="Расстояние в метрах между центром сортировки (заданной параметрами sort_point_lat, sort_point_lng) и указанным в вакансии адресом. В случае, если в адресе указаны только станции метро, выдается расстояние между центром сортировки и средней геометрической точкой указанных станций. Значение sort_point_distance выдается только в случае, если заданы параметры sort_point_lat, sort_point_lng, order_by=distance")
    counters: Optional[int] = Field(description="поле counters с количеством откликов для вакансии. ")
    snippet: Optional[dict] = Field(description="Дополнительные текстовые снипеты (отрывки) по найденной вакансии. Если в тексте снипета встретилась поисковая фраза (параметр text), она будет подсвечена тегом highlighttext.")


class VacancyHHSchema(ShortVacancyHHSchema):
    description: HTML = Field(description="Описание вакансии, содержит html")
    branded_description: Optional[HTML] = Field(description="Брендированное описание вакансии")
    key_skills: list[KeySkillHHSchema] = Field(description="Информация о ключевых навыках, заявленных в вакансии. Список может быть пустым.")
    schedule: IdNameHHSchema = Field(description="График работы. Элемент справочника schedule")
    accept_handicapped: bool = Field(description="Указание, что вакансия доступна для соискателей с инвалидностью")
    accept_kids: bool = Field(description="Указание, что вакансия доступна для соискателей от 14 лет")
    experience: IdNameHHSchema = Field(description="Требуемый опыт работы. Элемент справочника experience")
    code: Optional[str] = Field(description="Внутренний код вакансии работадателя")
    employment: Optional[IdNameHHSchema] = Field(description="Тип занятости. Элемент справочника employment.")
    created_at: datetime = Field(description="Дата и время создания вакансии")
    test: Optional[TestHHSchema] = Field(description="Информация о прикрепленном тестовом задании к вакансии. В случае отсутствия теста — null. В данный момент отклик на вакансии с обязательным тестом через API невозможен.")
    specializations: list[SpecializationHHSchema] = Field(description="Специализации. Элементы справочника specializations")
    contacts: Optional[ContactsHHSchema] = Field(description="Контактная информация")
    billing_type: IdNameHHSchema = Field(description="Биллинговый тип вакансии. Элемент справочника vacancy_billing_type.")
    allow_messages: bool = Field(description="Включена ли возможность соискателю писать сообщения работодателю, после приглашения/отклика на вакансию")
    # TODO: Элемент справочника driver_license_types https://github.com/hhru/api/blob/master/docs/dictionaries.md
    driver_license_types: list[dict] = Field(description="Список требуемых категорий водительских прав. Список может быть пустым.")
    accept_incomplete_resumes: bool = Field(description="Разрешен ли отклик на вакансию неполным резюме")
    professional_roles: list[IdNameHHSchema] = Field(description="Массив объектов профролей. Список может быть пустым.")
    suitable_resumes_url: Optional[HttpUrl]
    negotiations_url: Optional[HttpUrl]
    quick_responses_allowed: bool
    hidden: bool
    vacancy_constructor_template: Optional[dict]


class VacancySearchParamsHHSchema(BaseModel):
    """ При указании параметров пагинации (page, per_page) работает ограничение: глубина возвращаемых
    результатов не может быть больше 2000. Например, возможен запрос per_page=10&page=199
    (выдача с 1991 по 2000 вакансию), но запрос с per_page=10&page=200 вернёт ошибку (выдача с 2001 до 2010 вакансию).
    """
    text: Optional[str] = Field(description="Переданное значение ищется в полях вакансии, указанных в параметре search_field. Доступен язык запросов, как и на основном сайте: https://hh.ru/article/1175. Специально для этого поля есть автодополнение.")
    search_field: Optional[Union[str, list[str]]] = Field(description="область поиска. Справочник с возможными значениями: vacancy_search_fields в /dictionaries. По умолчанию, используются все поля. Возможно указание нескольких значений.")
    experience: Optional[str] = Field(description="Необходимо передавать id из справочника experience в /dictionaries.")
    employment: Optional[Union[str, list[str]]] = Field(description="тип занятости. Необходимо передавать id из справочника employment в /dictionaries. Возможно указание нескольких значений.")
    schedule: Optional[Union[str, list[str]]] = Field(description="график работы. Необходимо передавать id из справочника schedule в /dictionaries. Возможно указание нескольких значений.")
    area: Optional[Union[str, list[str]]] = Field(description="регион. Необходимо передавать id из справочника /areas. Возможно указание нескольких значений.")
    metro: Optional[Union[str, list[str]]] = Field(description="ветка или станция метро. Необходимо передавать id из справочника /metro. Возможно указание нескольких значений.")
    specialization: Optional[Union[str, list[str]]] = Field(description="профобласть или специализация. Необходимо передавать id из справочника /specializations. Возможно указание нескольких значений. Будет заменен профессиональными ролями (параметр professional_role), в настоящее время работает в режиме обратной совместимости.")
    industry: Optional[Union[str, list[str]]] = Field(description="индустрия компании, разместившей вакансию. Необходимо передавать id из справочника /industries. Возможно указание нескольких значений.")
    employer_id: Optional[Union[str, list[str]]] = Field(description="идентификатор компании. Возможно указание нескольких значений.")
    currency: Optional[str] = Field(description="код валюты. Справочник с возможными значениями: currency (ключ code) в /dictionaries. Имеет смысл указывать только совместно с параметром salary.")
    salary: Optional[int] = Field(description="Если указано это поле, но не указано currency, то используется значение RUR у currency. При указании значения будут найдены вакансии, в которых вилка зарплаты близка к указанной в запросе. При этом значения пересчитываются по текущим курсам ЦБ РФ. Например, при указании salary=100&currency=EUR будут найдены вакансии, где вилка зарплаты указана в рублях и после пересчёта в Евро близка к 100 EUR. По умолчанию будут также найдены вакансии, в которых вилка зарплаты не указана, чтобы такие вакансии отфильтровать, используйте only_with_salary=true.")
    label: Optional[Union[str, list[str]]] = Field(description="Необходимо передавать id из справочника vacancy_label в /dictionaries. Возможно указание нескольких значений.")
    only_with_salary: Optional[bool] = Field(description="показывать вакансии только с указанием зарплаты. Возможные значения: true или false. По умолчанию, используется false.")
    period: Optional[conint(ge=0, le=30)] = Field(description="количество дней, в пределах которых нужно найти вакансии. Максимальное значение: 30.")
    date_from: Optional[date] = Field(description="дата, которая ограничивает снизу диапазон дат публикации вакансий. Нельзя передавать вместе с параметром period. Значение указывается в формате ISO 8601 - YYYY-MM-DD или с точность до секунды YYYY-MM-DDThh:mm:ss±hhmm. Указанное значение будет округлено до ближайших 5 минут.")
    date_to: Optional[date] = Field(description="дата, которая ограничивает сверху диапазон дат публикации вакансий. Необходимо передавать только в паре с параметром date_from. Нельзя передавать вместе с параметром period. Значение указывается в формате ISO 8601 - YYYY-MM-DD или с точность до секунды YYYY-MM-DDThh:mm:ss±hhmm. Указанное значение будет округлено до ближайших 5 минут.")
    top_lat: Optional[float] = Field(description="top_lat, bottom_lat, left_lng, right_lng — значение гео-координат. При поиске используется значение указанного в вакансии адреса. Принимаемое значение — градусы в виде десятичной дроби. Необходимо передавать одновременно все четыре параметра гео-координат, иначе вернется ошибка.")
    bottom_lat: Optional[float] = Field(description="top_lat, bottom_lat, left_lng, right_lng — значение гео-координат. При поиске используется значение указанного в вакансии адреса. Принимаемое значение — градусы в виде десятичной дроби. Необходимо передавать одновременно все четыре параметра гео-координат, иначе вернется ошибка.")
    left_lng: Optional[float] = Field(description="top_lat, bottom_lat, left_lng, right_lng — значение гео-координат. При поиске используется значение указанного в вакансии адреса. Принимаемое значение — градусы в виде десятичной дроби. Необходимо передавать одновременно все четыре параметра гео-координат, иначе вернется ошибка.")
    right_lng: Optional[float] = Field(description="top_lat, bottom_lat, left_lng, right_lng — значение гео-координат. При поиске используется значение указанного в вакансии адреса. Принимаемое значение — градусы в виде десятичной дроби. Необходимо передавать одновременно все четыре параметра гео-координат, иначе вернется ошибка.")
    order_by: Optional[str] = Field(description="сортировка списка вакансий. Справочник с возможными значениями: vacancy_search_order в /dictionaries. Если выбрана сортировка по удалённости от гео-точки distance, необходимо также задать её координаты sort_point_lat,sort_point_lng.")
    sort_point_lat: Optional[float] = Field(description="значение гео-координат точки, по расстоянию от которой будут отсортированы вакансии. Необходимо указывать только, если order_by установлено в distance.")
    sort_point_lng: Optional[float] = Field(description="значение гео-координат точки, по расстоянию от которой будут отсортированы вакансии. Необходимо указывать только, если order_by установлено в distance.")
    clusters: Optional[bool] = Field(description="возвращать ли кластеры для данного поиска, по умолчанию: false.")
    describe_arguments: Optional[bool] = Field(description="возвращать ли описание использованных параметров поиска, по умолчанию: false.")
    per_page: Optional[conint(ge=0, le=100)] = Field(description="параметры пагинации. Параметр per_page ограничен значением в 100.")
    page: Optional[conint(ge=0)] = Field(description="параметры пагинации. Параметр per_page ограничен значением в 100.")
    no_magic: Optional[bool] = Field(description="Если значение true – отключить автоматическое преобразование вакансий. По умолчанию – false. При включённом автоматическом преобразовании, будет предпринята попытка изменить текстовый запрос пользователя на набор параметров. Например, запрос text=москва бухгалтер 100500 будет преобразован в text=бухгалтер&only_with_salary=true&area=1&salary=100500.")
    premium: Optional[bool] = Field(description="Если значение true – в сортировке вакансий будет учтены премиум вакансии. Такая сортировка используется на сайте. По умолчанию – false.")
    responses_count_enabled: Optional[bool] = Field(description="Если значение true – включить дополнительное поле counters с количеством откликов для вакансии. По-умолчанию – false.")
    # TODO: не понял как пользоваться part_time в поиске
    part_time: Optional[Union[str, list[str]]] = Field(description="Вакансии для подработки. Возможные значения: все элементы из working_days в /dictionaries. все элементы из working_time_intervals в /dictionaries. все элементы из working_time_modes в /dictionaries. элементы part или project из employment в /dictionaries. элемент accept_temporary, показывает вакансии только с временным трудоустройством. Возможно указание нескольких значений.")
    professional_role: Optional[Union[str, list[str]]] = Field(description="профессиональная роль. Необходимо передавать id из справочника professional_roles. Возможно указание нескольких значений. Замена специализациям (параметр specialization)")

    def get_params(self) -> str:
        params: str = ""
        for prop, value in vars(self).items():
            if value is None:
                continue
            if type(value) is list:
                for v in value:
                    params += f"&{prop}={v}"
            else:
                params += f"&{prop}={value}"
        return "?" + params[1:]


class ShortVacancyListHHSchema(BaseModel):
    items: list[ShortVacancyHHSchema]
    found: int
    pages: int
    per_page: int
    page: int
    clusters: Optional[dict]
    arguments: Optional[dict]
    alternate_url: HttpUrl


class EmployerHHSchema(ShortEmployerHHSchema):
    type: Optional[str] = Field(description="тип компании (прямой работодатель, кадровое агентство и т.п.). Возможные значения описаны в коллекции справочников под ключом employer_type. Возможно значение null, если тип компании скрыт.")
    site_url: HttpUrl = Field(description="адрес сайта компании")
    description: Optional[HTML] = Field(description="описание компании в виде строки с кодом HTML (без <script/> и <style/>)")
    branded_description: Optional[HTML] = Field(description="брендированное описание компании в виде строки с кодом HTML")
    trusted: bool = Field(description="флаг, показывающий, прошла ли компания проверку на сайте.")
    insider_interviews: list[InsiderInterviewHHSchema] = Field(description="список интервью или пустой список, если интервью отсутствуют")
    area: AreaHHSchema = Field(description="информация о регионе работодателя")
    relations: list[dict] = Field(description="если работодатель добавлен в черный список, то вернется ['blacklisted'] иначе []")
    industries: list[IdNameHHSchema] = Field(description="Cписок отраслей компании. Элементы справочника индустрий.")


class ShortEmployerListHHSchema(BaseModel):
    items: list[ShortEmployerHHSchema]
    found: int
    pages: int
    per_page: int
    page: int
