import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.book import Book  # noqa: E501
from openapi_server.models.create_book_request import CreateBookRequest  # noqa: E501
from openapi_server.models.update_book_request import UpdateBookRequest  # noqa: E501
from openapi_server import util


def create_book(body):  # noqa: E501
    """Create a new book

     # noqa: E501

    :param create_book_request: 
    :type create_book_request: dict | bytes

    :rtype: Union[Book, Tuple[Book, int], Tuple[Book, int, Dict[str, str]]
    """
    create_book_request = body
    if connexion.request.is_json:
        create_book_request = CreateBookRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_book(id):  # noqa: E501
    """Delete book by ID

     # noqa: E501

    :param id: 
    :type id: int

    :rtype: Union[None, Tuple[None, int], Tuple[None, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_book_by_id(id):  # noqa: E501
    """Get book by ID

     # noqa: E501

    :param id: 
    :type id: int

    :rtype: Union[Book, Tuple[Book, int], Tuple[Book, int, Dict[str, str]]
    """
    return 'do some magic!'


def get_books():  # noqa: E501
    """Get all books

     # noqa: E501


    :rtype: Union[List[Book], Tuple[List[Book], int], Tuple[List[Book], int, Dict[str, str]]
    """
    return 'do some magic!'


def update_book(id, body):  # noqa: E501
    """Update book by ID

     # noqa: E501

    :param id: 
    :type id: int
    :param update_book_request: 
    :type update_book_request: dict | bytes

    :rtype: Union[Book, Tuple[Book, int], Tuple[Book, int, Dict[str, str]]
    """
    update_book_request = body
    if connexion.request.is_json:
        update_book_request = UpdateBookRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
