import os
import gzip
import logging.handlers
import logging.config
from datetime import datetime

from bottle import request

log_file = os.environ.get('log_path')
print('log_file : {}'.format(log_file))


def create_version_conflict_details(obj_version, request_version):
    return {'object version': obj_version, 'request version': request_version}


def create_security_details(obj_domain_id, obj_security_tags):
    return {'object domain id': obj_domain_id,
            'object security tags': obj_security_tags}


def create_can_not_be_deleted_details(obj_id, error_msg):
    return {'id': obj_id, 'sql error': error_msg}


def get_request_id():
    try:
        if hasattr(request, 'JJP_RID'):
            return request.JJP_RID
    except RuntimeError:
        return 'NO_RID'


class GZipRotator:
    def __call__(self, source, dest):
        os.rename(source, dest)
        f_in = open(dest, 'rb')
        f_out = gzip.open("%s.gz" % dest, 'wb')
        f_out.writelines(f_in)
        f_out.close()
        f_in.close()
        os.remove(dest)


class JJPFormatter(logging.Formatter):
    def formatException(self, exc_info):
        """
        Format an exception so that it prints on a single line.
        """
        result = super(JJPFormatter, self).formatException(exc_info)
        return repr(result)  # or format into one line however you want to

    def format(self, record):
        s = super(JJPFormatter, self).format(record)
        s = "{} - {}".format(get_request_id(), s)
        if record.exc_text:
            s = s.replace('\n', '') + '|'
        return s


handler = logging.handlers.TimedRotatingFileHandler(log_file,
                                                    encoding='utf8',
                                                    when='Midnight',
                                                    interval=1,
                                                    backupCount=5)
logger = logging.getLogger(__name__)
fmtr = JJPFormatter(
    '%(asctime)s,%(msecs)d %(levelname)-2s[%(pathname)s :%(lineno)d - %(funcName)s] %(message)s')

handler.setFormatter(fmtr)
logger.addHandler(handler)
logging.basicConfig(
    filename=log_file,
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.DEBUG)


class LogMsg:
    START = "function is called -- user is : %s "
    END = "function finished successfully "
    ADDING_ERR = "adding model to database encountered a problem  "
    DATETIME_ADDITION = "date time added to model  "
    DATA_ADDITION = "data added to model : %s "
    DB_ADD = "model added to database : %s  "
    AUTH_CHECKING = "going to check authentication  "
    AUTH_SUCCEED = "authentication is successful  "
    GET_SUCCESS = "getting from database is successful : %s "
    GET_FAILED = "getting from database failed : %s "
    DELETE_SUCCESS = "deleting item is done successfully  "
    DELETE_FAILED = "deleting the item encountered a problem "
    DELETE_REQUEST = "request for deleting item : %s"
    EDIT_REQUST = "editing the item : %s"
    EDIT_SUCCESS = "editing item is done successfully  "
    EDIT_FAILED = "editing the item encountered a problem  "
    MODEL_GETTING = "model_instance getting from database by id : %s "
    MODEL_GETTING_FAILED = "item is not exists in database  "
    MODEL_ALTERED = "item altered successfully : %s "
    GET_ALL_REQUEST = "getting all request from db..."
    NOT_FOUND = "no such item exists : %s"
    COMMIT_FAILED = 'commiting process failed'
    TOKEN_CREATED = 'a new token for user created'
    TOKEN_EXPIRED = 'token is expired'
    TOKEN_DELETED = 'token deleted successfuly'
    TOKEN_INVALID = 'token is invalid'
    ALTERING_AUTHORITY_FAILED = 'user has no admission to alter the item'
    DELETE_PROCESSING = 'going to delete the item from db'
    GATHERING_RELATIVES = 'gathering item reletives to delete them from db'
    DELETE_RELATIVE = 'the reletive %s is going to be delete'
    UPLOAD_NOT_ALLOWED = 'no more uploads supports in edit'
    POST_ALREADY_LIKED = 'user liked the post before'
    USER_XISTS = 'user by this username : %s already exists'
    PARENT_INVALID = 'parent entity doesnt exist'
    CHECK_REDIS_FOR_EXISTANCE = 'checking redis if cell number already ' \
                                'exists...'
    INVALID_ENTITY_TYPE = 'the entity type is invalid : %s'
    REGISTER_XISTS = 'user has already valid registery code'
    CHECK_USER_EXISTANCE = 'checking user if already exists'
    GENERATING_REGISTERY_CODE = 'generating key for registering process for ' \
                                'cell no : %s'
    SEND_CODE_BY_SMS = 'registery activation_code is going to send for user by SMS'
    SMS_SENT = 'message sent to user by cell no : %s'
    MESSAGE_SENT = 'sms sent and response by operator is : %s'
    DATA_MISSING = 'required data doesnt exists in data : %s'
    REGISTER_KEY_INVALID = 'your register activation_code is wrong '
    REGISTER_KEY_DOESNT_EXIST = 'the activation_code expired or doesnt exist '
    USR_ADDING = 'user is going to create...'
    USER_BY_CELL_EXIST = 'user with this cell no already exist'
    NOT_UNIQUE = 'must be unique,change it please'
    NOT_ACCESSED = 'this user can not access to this section'
    SCROLL_UNDEFINED = 'scrolling mood is undefined.it should be up or down'
    SCHEMA_CHECKED = 'schema checked for required data'
    USERNAME_NOT_UNIQUE = 'this username already exists'
    TOKEN_KEY_DOESNT_EXIST = 'the token is expired or doesnt exists'
    PERSON_EXISTS = 'person by this username : %s exists'
    NOT_RIGTH_ENTITY_PASSED = 'your entity type is not %s'
    PERSON_NOT_EXISTS = 'person for this username not exists : %s '
    NOT_EDITABLE = 'field is not editable'
    ENTITY_DELETED = 'the entity deleted successfully : %s'
    RELATED_USER_DELETE = 'related user_id of person is %s is going to delete'
    USER_HAS_SIGNUP_TOKEN = 'user has sign up token and new code cant send'
    USER_HAS_ACTIVATION_CODE = 'user already has valid activation code and cant resend code now'
    ENUM_CHECK = 'checking enums to be right type  -  %s'
    USER_CHECKING = 'checking user by username :  %s'
    INVALID_USER = 'user by this username doesnt exist : %s'
    POPULATING_BASIC_DATA = 'new model is populating with basic data'
    EDITING_BASIC_DATA = 'editing basic data for model : %s'

    # Account
    GETTING_USER_ACCOUNTS = 'getting acount of user by type  : %s '
    ACCOUNT_BY_TYPE_EXISTS = 'user has already an account of type : %s '
    GETTING_PERSON_ALL_ACCOUNTS = 'getting all acounts of person_id : %s'
    DELETE_USER_ALL_ACCOUNTS = 'deleting users all accounts username is : %s '
    DELETE_ACCOUNT_BY_ID = 'deleting account by id = %s '
    GETTING_ACCOUNT_BY_ID = 'getting account by id = %s '
    EDIT_ACCOUNT_VALUE = 'changing account value : %s '
    ACCOUNT_VALUE_EDITED = 'the value if account : %s changed successfully'
    ACCOUNT_BY_ID_IS_NOT_FOR_PERSON = 'the account doesnt exist or not owned by user : %s '
    ADD_INITIAL_ACCOUNT = 'adding initial account of type Main for person_id : %s '
    GETTING_ACCOUNT_PERSON = 'getting account by data : %s'
    USER_HAS_NO_ACCOUNT = 'user has no account of type: %s'

    # Token
    CHECKING_VALID_TOKEN = 'checking if user: %s has valid token '
    USER_HAS_VALID_TOKEN = 'user already has valid token : %s '

    # BOOK
    ADD_BOOK = 'adding book by data : %s '
    DELETE_BOOK_FILES = 'deleting files of book by id : %s'
    DELETE_BOOK_IMAGES = 'deleting images of book by id : %s '
    EDITING_BOOK = 'editing book : %s '
    DELETING_BOOK = 'deleting book by id : %s '
    GETTING_ALL_BOOKS = 'request for getting all books'
    ADDING_MULTIPLE_BOOKS = 'adding multiple books by data : %s '
    ADDING_ROLES_TO_BOOK = 'adding roles to book : %s '
    ATTACHING_ROLES_TO_BOOKS = 'attaching book roles to book entities'
    DELETING_BOOK_ROLES = 'deleting roles of book by id : %s '
    DELETING_BOOK_COMMENTS = 'deleting comments of book : %s '
    DELETING_BOOK_PRICE = 'deleting price of book : %s '
    SEARCH_BOOK_BY_TITLE = 'searching books by titles like : %s '
    SEARCH_BOOK_BY_GENRE = 'searching books by genre like : %s '
    SEARCH_BOOK_BY_PHRASE = 'searching for books by phrase : %s '
    SEARCH_BOOK_BY_TAGS = 'searching for books by tag : %s '
    SEARCH_BOOKS = 'searching for books by filter : %s'
    GETTING_BOOKS_FROM_LIST = 'getting books from list id ids : %s'
    GETTING_NEWEST_BOOKS = 'getting newest book list'
    RESULT_BOOKS = 'result of books is : %s'
    BOOK_CHECKING_IF_EXISTS = 'checking for uniqueness of book : %s'
    BOOK_NOT_UNIQUE = 'book is not unique and already exists : %s'
    BOOK_ONLINE_TYPE_COUNT_LIMITATION = 'online book types can not have count greater than one'
    BOOK_INDEX_EXISTS = 'book index in elastic already exists :%s'
    BOOK_INDEXED = 'book is indexed in elastic by data : %s'

    # BOOK_ROLE
    ADDING_ROLES_OF_BOOK = 'adding roles of a book to DB by list : %s'
    ROLE_ADDED = 'role added to book : %s'
    DELETE_BOOK_ROLES = 'deleting all roles for book : %s '
    GET_PERSONS_BOOKS = 'getting all books which person has a role in . the person is : %s'
    PERSON_BOOK_LIST = 'persons list of books which has a role in is : %s '
    GETTING_ROLES_OF_BOOK = 'getting all roles of book : %s'
    BOOKS_ROLES = 'the roles of book is : %s'

    # COMMENT
    COMMENT_VALIDATING_BOOK = 'getting book to validate commenting : %s'
    COMMENT_CHECK_FOR_PARENT = 'checking if comment has a parent'
    COMMENT_GETTING_PARENT = 'getting comment parent by id : %s'
    COMMENT_PARENT_NOT_FOUND = 'comments parent by this id not found : %s'
    COMMENT_PARENT_NOT_MATCH = 'this parent comment is not matching for this book id : %s'
    COMMENT_DELETING_BOOK_COMMENTS = 'deleting all comments of book by id : %s '
    COMMENT_GETTING_BOOK_COMMENTS = 'getting all comments of book by id :%s '
    COMMENT_DELETE_ACTIONS = 'deleting comment actions for comment : %s'
    COMMENT_DELETE = 'deleting comment by id : %s'

    # COMMENT_ACTION

    ACTION_CHECK_COMMENT = 'checking for comment existance by id : %s'
    ACTION_REPORT_COMMENT = 'reporting comment by id : %s '
    ACTION_DISREPORT_COMMENT = 'disreporting comment by id : %s '
    ACTION_LIKE_COMMENT = 'liking comment by id : %s'
    ACTION_DISLIKE_COMMENT = 'disliking comment by id : %s '
    ACTION_GETTING_LIKES = 'getting comment likes by id : %s'
    ACTION_GETTING_REPORTS = 'getting comment reports by id : %s '
    ACTION_CHECK_USER_LIKED = 'checking if user liked comment already : %s'
    ACTION_CHECK_USER_REPORTED = 'checking if user reported the comment : %s '
    ACTION_ALREADY_LIKED = 'user already liked the comment '
    ACTION_ALREADY_REPORTED = 'user already reported the comment'
    ACTION_USER_CANT_DISLIKE = 'user not liked the comment so cant dislike it'
    ACTION_USER_CANT_DISREPORT = 'user not reported the comment so cant desreport it'

    # Price
    ADDING_PRICE = 'adding price for book : %s '
    CHECK_BOOK_PRICE_EXISTANCE = 'checking if book already has price in db : %s'
    BOOK_PRICE_EXISTS = 'book by this id already has price: %s'
    EDIT_PRICE = 'editing book price by id : %s'
    ADD_NEW_BOOK_PRICE = 'adding new price entity for book : %s'
    PRICE_NOT_FOUND = 'no price found for this book : %s'
    PRICE_ITEM_CALC = 'price calculated for item is : %s'
    PRICE_ALL_CALCED = 'total price calced successfully : %s'
    PRICE_CALC_FAILED = 'calculating price failed. '
    PRICE_NET_CALCED = 'net price calced for data : %s '

    # Elasticsearch
    INDEXING_IN_ELASTIC = 'indexing book data in elastic search : %s '
    ELASTIC_INDEX_DELETE = 'deleting book index in elastic search by id : %s'
    SEARCH_ELASTIC_INDEXES = 'searching in elastic search for indexes by phrase : %s '
    ELASTIC_SEARCH_RESULTS = 'elastic search result for book_id s is : %s '

    # USER
    USER_HAS_NO_PERSON = 'user by ths username has no related person : %s '
    NOT_RELATED_USER_FOR_PERSON = 'person has not related user : %s'
    USER_GENERATING = 'generating user in signup by data : %s'
    USER_PROFILE_IS = 'users profile is : %s'
    USER_GET_BY_FILTER = 'searching user by filter like : %s'
    USER_PASSWORD_RESET = 'users password changed successfully : %s'

    # PERSON
    PERSON_HAS_BOOKS = 'person already has roles for books '
    PERSON_GENERATING = 'generating person in signup by data : %s'
    PERSON_ADD_ACCOUNT = 'added initial account of type main for person : %s'
    PERSON_ACCOUNTS_DELETED = 'person accounts deleted : %s'
    PERSON_DELETED = 'person by id : %s deleted successfully'
    PERSON_USERS_GOT = 'users of person : %s got successfully'
    ANOTHER_PERSON_BY_CELL = 'another person exists by this cell_no'
    LEGAL_PERSON_USER_RESTRICTION = 'legal persons cannot have more than 1 user'
    PERSON_IS_NOT_LEGAL = 'person is not legal :  %s'
    PERSON_MUST_HAVE_USER = 'person must have user : %s'

    # UNIQUE CONSTRAINT
    GENERATE_UNIQUE_CONSTRAINT = 'generating unique constraint key for entity by data : %s'
    DELETE_UNIQUE_CONSTRAINT = 'deleting unique constraint key for entity by data : %s'
    CHECK_UNIQUE_EXISTANCE = 'checking for existance of unique code : %s'
    UNIQUE_CONSTRAINT_EXISTS = 'the unique costraint key already exists : %s'
    UNIQUE_CONSTRAINT_IS = 'the unique constraint generated is :%s '
    UNIQUE_CONSTRAINT_IS_CHANGING = 'unique constraint is changing by deleting old one and generating new one'
    UNIQUE_CONNECTOR_ADDED = 'the unique_connector added for this model : %s'
    UNIQUE_NOT_EXISTS = 'unique constraint not exists'

    # LIBRARY
    LIBRARY_CHECK_BOOK_EXISTANCE = 'checking if book already is in library : %s'
    LIBRARY_BOOK_TYPE_NOT_ADDABLE = 'this type of book is not addable to library : %s'
    ALREADY_IS_IN_LIBRARY = 'book is already purchased and is in library : %s'
    LIBRARY_GET_PERSON_LIBRARY = 'getting library contents for person by username : %s'
    LIBRARY_ADD_BOOKS = 'adding books to persons library : %s'

    # COLLECTION
    COLLECTION_ADD_NEW_COLLECTION = 'adding new collection by title : %s'
    COLLECTION_ADD_BOOKS_TO_COLLECTION = 'adding books to collection: %s'
    COLLECTION_CHECK_BOOK_IS_IN_COLLECTION = 'check if book is in collection : %s'
    COLLECTION_BOOK_ALREADY_EXISTS = 'book already is in collection : %s'
    COLLECTION_GET = 'getting books of a collection : %s'
    COLLECTION_DELETE = 'deleting collection by title : %s'
    COLLECTION_GET_ALL = 'getting all collections %s'
    COLLECTION_DELETE_BOOK = 'deleting books from a collection : %s'
    COLLECTION_ADD_BOOK_TO_MULTIPLE_COLLECTIONS = 'adding book to multiple collections : %s'
    COLLECTION_BOOK_IS_NOT_IN_LIBRARY = 'this book is not in users library : %s'
    COLLECTION_ADD_EMPTY_COLLECTION = 'adding an empty collection for user : %s '
    COLLECTION_ARRANGE_BY_TITLE = 'arranged collection contents by title'
    COLLECTION_EXISTS = 'collection by this title already exists : %s'

    # RATE
    RATE_CHECK = 'checking if person rated to book by now : %s'
    RATE_EXISTS = 'user already rated to book : %s'
    RATE_IS_NEW = 'user is not rated to the book and going to do that : %s'
    RATE_CHANGED = 'user is changing the rate of book : %s'
    RATE_ADDED = 'new rate to book added : %s'
    RATE_DELETED = 'user deleted the rate for book : %s'
    RATE_GET = 'getting book rate : %s'
    RATE_NOT_EXISTS = 'user not rated to the book : %s'

    # TRANSACTION
    TRANSACTION_ADDED = 'transaction added by this data : %s'
    TRANSACTION_GET = 'getting transaction by data : %s'
    TRANSACTION_EXISTS = 'transaction exists : %s'
    TRANSACTION_DELETED = 'transaction by this id deleted : %s'

    # FOLLOW
    FOLLOW_REQUEST = 'following request by data : %s'
    FOLLOW_ADD = 'follow added by data :%s'
    FOLLOW_DELETE = 'user unfollowed the person : %s'
    FOLLOW_CHECK = 'checking if user is following person : %s'
    FOLLOW_EXISTS = 'user already follows the person : %s'
    FOLLOW_SELF_DENIED = 'user cannot follow him/her self'
    FOLLOWING_LIST = 'get users following list : %s'
    FOLLOWER_LIST = 'get follower list : %s'

    # ORDER
    ORDER_CHECKOUT_REQUEST = 'request for checking out order by id : %s'
    ORDER_CHECK = 'check for order existance by id : %s'
    ORDER_EXISTS = 'order by id exists : %s'
    ORDER_ADD = 'order added by data : %s'
    ORDER_CALC_PRICE = 'calculating order price : %s'
    ORDER_CHECK_ACCOUNT_VALUE = 'checking users account balance to be greater than order price : %s'
    ORDER_LOW_BALANCE = 'users account balance is lower than order price : %s'
    ORDER_INVOICED = 'order invoiced successfully : %s'
    ORDER_GETTING_ITEMS = 'getting order_items to add to users library '
    ORDER_ITEMS_ADDED_TO_LIB = 'books added to library successfully'
    ORDER_CHECK_ITEM_TYPE = 'check if book type is addable to library : %s'
    ORDER_ADD_ITEMS = 'adding order items to db: %s'
    ORDER_USER_ORDERS = 'user orders are : %s'
    ORDER_NOT_EDITABLE = 'order is invoiced and can not be edited or deleted : %s'
    ORDER_ITEMS_DELETE = 'deleting order items : %s'
    ORDER_DELETE = 'deleting order: %s'
    ORDER_EDIT = 'editing order : %s'
    ORDER_ITEM_ADDDED_TO_ORDER = 'order_item added to order : %s'
    ORDER_TOTAL_PRICE = 'order total price is : %s'
    ORDER_ITEM_UNIT_PRICE = 'order items unit price got : %s'
    ORDER_ITEM_NET_PRICE = 'order items net price calculated : %s '
    ORDER_ITEM_DELETED = 'order item by id: %s deleted'
    ORDERS_ITEMS = 'orders items collected successfully : %s '

    # REGISTER
    MESSAGE_NOT_SENT = 'message not sent by data : %s'
    REDIS_SET = 'setting reset pass key in redis : %s'

    # SIGNUP
    SIGNUP_GETTING_TOKEN_FROM_REDIS = 'getting signup token from redis by cell_no: %s'
    SIGNUP_TOKEN_NOT_IN_REDIS = 'there is no signup token in redis for this cell_no :%s'
    SIGNUP_TOKEN_INVALID = 'signup token not send correctly and is not compatible by redis data : %s'
    SIGNUP_SUCCESS = 'signup process finished successfully : %s'

    # WISH LIST
    WISH_CHECK_IF_IN_LIST = 'checking if book is in wish list of user already : %s'
    WISH_ALREADY_EXISTS = 'book is already in wish list of user :%s'
    WISH_ADD = 'book added to users wish list : %s'
    WISH_GET = 'getting wish list of user :%s'
    WISH_IS = 'users wish list is : %s'
    WISH_DELETE = 'book deleted from users widh list : %s'
    WISH_DELETE_ALL = 'deleting wish list of user : %s'

    # GROUP
    GROUP_EXISTS = 'group by this data already exists : %s'
    GROUP_INVALID = 'group by this data not exists : %s'
    GROUP_DELETE = 'group by id = %s is going to be deleted ...'
    GROUP_DELETE_PERMISSIONS = 'deleting all permissions of group : %s'

    # GROUP USER
    GROUP_USER_IS_IN_GROUP = 'user already is in group : %s'
    GROUP_USER_NOT_IN_GROUP = 'user not in group and cant be deleted : %s'
    DELETE_GROUP_USERS = 'deleting group_users first : %s'
    GROUP_DELETE_USER_GROUPS = 'deleting user by id = %s from groups ...'

    # PERMISSION
    PERMISSION_NOT_HAS_GROUP = 'group has no permission by data : %s'
    PERMISSION_GROUP_ALREADY_HAS = 'group already has this permission : %s'
    PERMISSION_CHECK = 'checking permission of user : %s'
    PERMISSION_DENIED = 'user has no permission for action : %s'
    PERMISSION_VERIFIED = 'user has permission for vthe action : %s'
    PREMIUM_PERMISSION_ADDITION_RESTRICTION = 'user with not premium permission cant assign premium permission to group : %s'
    PREMIUM_PERMISSION_NOT_FOUND = 'user has no premium permission by data : %s'

    # DISCUSSION_GROUP
    DISCUSSION_GROUP_ADD = 'discussion group added by data : %s'
    DISCUSSION_GROUP_MEMBERS_ADDED = 'members added to group : %s'
    DISCUSSION_GROUP_NOT_ADMIN = 'user is not admin of group and cant change group properties: %s'
    DISCUSSION_GROUP_OLD_MEMBERS_DELETED = 'members of group deleted successfully ...'
    DISCUSSION_GROUP_DELETE = 'discussion group deleted successfully : %s'

    # CHAT MESSAGING
    CHAT_PERSON_NOT_IN_GROUP = 'sender is not in group: %s'
    CHAT_CHECK_FOR_PARENT = 'checking for existance of parent message --'
    CHAT_PARENT_EXISTS = 'parent of message exists by id : %s'
    CHAT_PARENT_NOT_FOUND = 'chat parent not found by id : %s'
    CHAT_GET_GROUP_MESSAGES = 'getting group messages by id : %s'
    CHAT_GET_USER_MESSAGES = 'getting messages of person by id : %s'

    LAST_SEEN_UPDATE = 'updating last_seen time of user by data: %s'
    LAST_SEEN_ADD = 'last_seen record added to table by data : %s'

    # PAYMENT
    PAYMENT_FAILED_KIPO = 'payment by kipo failed : %s'
    KIPO_PAYMENT_INITIATED = 'KIPO pyment gate initiated successfully : %s'
    ADDING_PAYMENT_ENTITY = 'payment entity is adding by data : %s'
    PAYMENT_ADDED = 'payment entity added successfuly :%s'
    PAYMENT_DATA_NOT_RECIEVED = 'payment data not recieved from bank gateway properly...'
    PAYMENT_CANCELED = 'payment canceled and no transaction occured in bank : %s'
    PAYMENT_NOT_FOUND = 'payment by the shopping_key %s not found in DB...'
    PAYMENT_ALREADY_USED = 'payment by this shopping key used already : %s'
    PAYMENT_UPDATED_TO_USED = 'payment entity updated to used : %s'
    PAYMENT_INQUIRY_NOT_VALID = 'payment inquiry from kipo is not valid: %s'
    PAYMENT_INQUIRY_AMOUNT_INVALID = 'payment amount in inquiry not equal with payment in DB : %s'
    PAYMENT_STATUS_NONE = 'payment status is None in url : %s'
    REDIRECT_AFTER_PAYMENT = 'payment is completed and user is redirecting to page : %s'
    CALL_BACK_FROM_BANK_URL = 'bank call back url is : %s'
    CALL_BACK_APP_URL = 'call back url of APP is : %s'
    PAYMENT_ENTITY_GET = 'payment entity got successfully : %s'
    PARSED_URL = 'parsed url of redirection is : %s'
    PAYMENT_STATUS = 'payment status is : %s'
    PAYMENT_INQUIRY_RESULT = 'payment inquiry result is : %s'

    # BOOK CONTENT
    CONTENT_EXIST = 'book content ba data exists : %s'
    DELETING_BOOK_CONTENT = 'deleteing contents of book by id : %s'
    BOOK_CONTENT_ALREADY_EXISTS = 'content entity by data already exists and its : %s'
    CONTENT_ALREADY_GENERATED = 'this content is generated already successfully ...'
    CONTENT_GENERATING = 'content generation process is working -- plz wait'
    BOOK_GENERATE_FAILED = 'generating book content failed: %s'
    RUN_PROCESS_DATA = 'data for running process of book generation is : %s'
    CONTENT_NOT_GENERATED = 'content of book not generated yet : %s'
    CONTENT_NOT_FOUND = 'content not found for book : %s'

    # DEVICE CODE

    MAXIMUM_ACTIVE_DEVICE = 'maximum device per user is already active : %s'
    USER_DEVICE_COUNT = 'number of users active devices is : %s'

    # BOOK PREPARE
    PREPARE_FULL_CONTENT = 'preparing full content for the owner of book: %s'
    PREPARE_ORIGINAL_ADDED = 'books original file prepared for download in : %s'
    PREPARE_BRIEF_ADDED = 'books brief file preparde for download in : %s'
    ALREADY_PREPARED = 'book content already prepared: %s'
    CHECK_FILE_EXISTANCE = 'checking for the existance of content for preparation : %s'

    # REPORTS
    REPORT_BOOK_OF_WEEK = 'book of week report : %s'
    REPORT_BOOK_OF_MONTH = 'book of month report : %s'
    USER_PERFORMANCE_REPORT = 'user performance report data : %s'

    # RID
    RID_OPERATION_FAILED = 'attaching request ID to request failed : %s'

    UPLOAD_FAILED = 'uploading files failed'
    FILE_EXISTS = 'this file exists by path : %s'
    FILE_NOT_EXISTS = 'file by this path not exists: %s'
    GET_FILE_FAILED = 'file can not be got'
    APP_CONFIG_INCORRECT = 'APP Config is incomplete : %s'

    NO_CONTENT_FOR_REPORT = 'there is no content in table %s for generating csv file'

    COMMIT_ERROR = 'commiting to db encountered problem'
    QUERY_OBJECT = 'query object is : %s'
    SCHEMA_NOT_VALID = 'data schema is not valid --- %s'
