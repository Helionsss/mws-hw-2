from uuid import uuid4

from api.graphql_api import GraphQLApi

HELLO_QUERY = "query { hello }"

CREATE_PERSON_MUTATION = """
mutation CreatePerson($person: PersonInput!) {
  createPerson(person: $person) {
    id
    name
    age
  }
}
"""

UNKNOWN_FIELD_QUERY = "query { fieldThatDoesNotExist }"


def test_hello_query_returns_data_without_errors():
    response = GraphQLApi().execute(HELLO_QUERY)
    assert response.status_code == 200, response.text
    payload = response.json()
    assert "errors" not in payload, payload
    assert payload.get("data", {}).get("hello") == "Hello John Doe", payload


def test_create_person_mutation_returns_created_person():
    person = {"name": f"Autotest Person {uuid4()}", "age": 30}
    response = GraphQLApi().execute(CREATE_PERSON_MUTATION, {"person": person})
    assert response.status_code == 200, response.text
    payload = response.json()
    assert "errors" not in payload, payload
    created_person = payload.get("data", {}).get("createPerson")
    assert isinstance(created_person, dict), payload
    assert str(created_person.get("id", "")).strip(), created_person
    assert created_person.get("name") == person["name"], created_person
    assert created_person.get("age") == person["age"], created_person


def test_unknown_field_query_returns_graphql_errors():
    response = GraphQLApi().execute(UNKNOWN_FIELD_QUERY)
    assert response.status_code == 200, response.text
    assert response.json().get("errors"), response.text
