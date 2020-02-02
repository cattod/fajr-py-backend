import enum
from helper import Http_error
from messages import Message


class Roles(enum.Enum):
    Author = 'Author'
    Writer = 'Writer'
    Translator = 'Translator'
    Press = 'Press'
    Contributer = 'Contributer'
    Designer = 'Designer'
    Narrator = 'Narrator'


class BookTypes(enum.Enum):
    DVD = 'DVD'
    Audio = 'Audio'
    Hard_Copy = 'Hard_Copy'
    Pdf = 'Pdf'
    Epub = 'Epub'
    Msd = 'Msd'


class BookContentType(enum.Enum):
    Brief = 'Brief'
    Original = 'Original'


class Genre(enum.Enum):
    Comedy = 'Comedy'
    Drama = 'Drama'
    Romance = 'Romance'
    Social = 'Social'
    Religious = 'Religious'
    Historical = 'Historical'
    Classic = 'Classic'
    Science = 'Science'


class ReportComment(enum.Enum):
    Personal = 'Personal'
    Invalid_Content = 'Invalid_Content'
    General = 'General'


class AccountTypes(enum.Enum):
    Main = 'Main'
    Star = 'Star'
    Discount = 'Discount'
    Postpaid = 'Postpaid'
    Prepaid = 'Prepaid'


class OrderStatus(enum.Enum):
    Created = 'Created'
    Invoiced = 'Invoiced'
    Canceled = 'Canceled'
    Postponed = 'Postponed'


class Access_level(enum.Enum):
    Premium = 'Premium'
    Press = 'Press'
    Normal = 'Normal'


class Permissions(enum.Enum):
    IS_OWNER = 'IS_OWNER'
    IS_MEMBER = 'IS_MEMBER'
    PERSON_ADD_PREMIUM = 'PERSON_ADD_PREMIUM'
    PERSON_EDIT_PREMIUM = 'PERSON_EDIT_PREMIUM'
    PERSON_DELETE_PREMIUM = 'PERSON_DELETE_PREMIUM'
    PERSON_GET_PREMIUM = 'PERSON_GET_PREMIUM'

    USER_DELETE_PREMIUM = 'USER_DELETE_PREMIUM'
    USER_GET_PREMIUM = 'USER_GET_PREMIUM'
    USER_EDIT_PREMIUM = 'USER_EDIT_PREMIUM'
    USER_GET_PRESS = 'USER_GET_PRESS'

    PERMISSION_GROUP_ADD_PREMIUM = 'PERMISSION_GROUP_ADD_PREMIUM'
    PERMISSION_GROUP_ADD_PRESS = 'PERMISSION_GROUP_ADD_PRESS'
    PERMISSION_GROUP_USER_DELETE_PREMIUM = 'PERMISSION_GROUP_USER_DELETE_PREMIUM'
    PERMISSION_GROUP_USER_ADD_PREMIUM = 'PERMISSION_GROUP_USER_ADD_PREMIUM'
    PERMISSION_GROUP_USER_DELETE_PRESS = 'PERMISSION_GROUP_USER_DELETE_PRESS'
    PERMISSION_GROUP_USER_ADD_PRESS = 'PERMISSION_GROUP_USER_ADD_PRESS'
    PERMISSION_GROUP_USER_GET_PREMIUM = 'PERMISSION_GROUP_USER_GET_PREMIUM'
    PERMISSION_GROUP_USER_GET_PRESS = 'PERMISSION_GROUP_USER_GET_PRESS'
    PERMISSION_GROUP_GET_PREMIUM = 'PERMISSION_GROUP_GET_PREMIUM'
    PERMISSION_GROUP_GET_PRESS = 'PERMISSION_GROUP_GET_PRESS'
    PERMISSION_GROUP_EDIT_PREMIUM = 'PERMISSION_GROUP_EDIT_PREMIUM'
    PERMISSION_GROUP_EDIT_PRESS = 'PERMISSION_GROUP_EDIT_PRESS'
    PERMISSION_GROUP_DELETE_PREMIUM = 'PERMISSION_GROUP_DELETE_PREMIUM'
    PERMISSION_GROUP_DELETE_PRESS = 'PERMISSION_GROUP_DELETE_PRESS'

    GROUP_PERMISSION_GET_PREMIUM = 'GROUP_PERMISSION_GET_PREMIUM'
    GROUP_PERMISSION_GET_PRESS = 'GROUP_PERMISSION_GET_PRESS'
    GROUP_PERMISSION_DELETE_PREMIUM = 'GROUP_PERMISSION_DELETE_PREMIUM'
    ASSIGN_PREMIUM_PERMISSION_GROUP_PREMIUM = 'ASSIGN_PREMIUM_PERMISSION_GROUP_PREMIUM'

    PERMISSION_GET_PREMIUM = 'PERMISSION_GET_PREMIUM'
    PERMISSION_ADD_PREMIUM = 'PERMISSION_ADD_PREMIUM'
    PERMISSION_EDIT_PREMIUM = 'PERMISSION_EDIT_PREMIUM'
    PERMISSION_DELETE_PREMIUM = 'PERMISSION_DELETE_PREMIUM'
    PERMISSION_GET_PRESS = 'PERMISSION_GET_PRESS'

    ADD_MOVIE_PREMIUM = 'ADD_MOVIE_PREMIUM'
    GET_MOVIE_PREMIUM = 'GET_MOVIE_PREMIUM'
    EDIT_MOVIE_PREMIUM = 'EDIT_MOVIE_PREMIUM'
    DELETE_MOVIE_PREMIUM = 'DELETE_MOVIE_PREMIUM'


def check_enums(data, enum_class):
    for type in data:
        if type not in enum_class.__members__:
            raise Http_error(404, Message.INVALID_ENUM)
    return data


def str_genre(genre_list):
    res = []
    if genre_list is None:
        genre_list = []
    for genre in genre_list:
        res.append((getattr(Genre, genre)).value)
    return res


def str_type(btype):
    if btype is not None:
        return (getattr(BookTypes, btype)).value
    else:
        return ''


def str_role(role):
    if role is not None:
        return (getattr(Roles, role)).value
    else:
        return ''


def str_report(report):
    if report is not None:
        if isinstance(report, str):
            return report
        else:
            return report.value
    else:
        return None


def check_enum(type, enum_class):
    if type not in enum_class.__members__:
        raise Http_error(404, Message.INVALID_ENUM)

    return type


def str_account_type(account_type):
    if account_type is not None:
        if isinstance(account_type, str):
            return account_type
        else:
            return account_type.value
    else:
        return None
