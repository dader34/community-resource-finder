#!/usr/bin/python
import json
from main import load_resources


def test_load_resources():
    resources = load_resources()
    assert isinstance(resources, list), "Resources should be a list"
    assert len(resources) > 0, "Resources should not be empty"
    assert len(resources) == 50, "Should have 50 resources"
    print("PASS: load_resources")


def test_required_keys():
    resources = load_resources()
    required_keys = ['name', 'category', 'address', 'phone', 'languages', 'zip']
    for resource in resources:
        for key in required_keys:
            assert key in resource, f"'{resource.get('name', 'unknown')}' missing key: {key}"
    print("PASS: required_keys")


def test_languages_are_lists():
    resources = load_resources()
    for resource in resources:
        assert isinstance(resource['languages'], list), f"Languages for '{resource['name']}' should be a list"
        assert len(resource['languages']) > 0, f"'{resource['name']}' should have at least one language"
    print("PASS: languages_are_lists")


def test_categories_exist():
    resources = load_resources()
    expected = ['Food', 'Free Clinics', 'Legal Aid', 'Shelters', 'ESL']
    found = set(r['category'] for r in resources)
    for category in expected:
        assert category in found, f"Missing category: {category}"
    print("PASS: categories_exist")


def test_filter_by_category():
    resources = load_resources()
    food = [r for r in resources if r['category'] == 'Food']
    assert len(food) > 0, "Should find food resources"
    fake = [r for r in resources if r['category'] == 'Fake Category']
    assert len(fake) == 0, "Fake category should return empty"
    print("PASS: filter_by_category")


def test_search_by_name():
    resources = load_resources()
    matched = [r for r in resources if 'library' in r['name'].lower()]
    assert len(matched) > 0, "Should find results for 'library'"
    no_match = [r for r in resources if 'xyznonexistent' in r['name'].lower()]
    assert len(no_match) == 0, "Garbage search should return empty"
    print("PASS: search_by_name")


def test_search_case_insensitive():
    resources = load_resources()
    upper = [r for r in resources if 'EVERETT' in r['name'].upper()]
    lower = [r for r in resources if 'everett' in r['name'].lower()]
    assert len(upper) == len(lower), "Search should be case insensitive"
    print("PASS: search_case_insensitive")


def test_filter_by_language():
    resources = load_resources()
    english = [r for r in resources if 'English' in r['languages']]
    assert len(english) == len(resources), "All resources should support English"
    spanish = [r for r in resources if 'Spanish' in r['languages']]
    assert len(spanish) > 0, "Should find Spanish resources"
    fake = [r for r in resources if 'Klingon' in r['languages']]
    assert len(fake) == 0, "Fake language should return empty"
    print("PASS: filter_by_language")


def test_zip_codes():
    resources = load_resources()
    for resource in resources:
        assert isinstance(resource['zip'], str), f"ZIP for '{resource['name']}' should be a string"
        assert len(resource['zip']) == 5, f"ZIP for '{resource['name']}' should be 5 digits"
    filtered = [r for r in resources if r['zip'] == '98201']
    assert len(filtered) > 0, "Should find resources in 98201"
    print("PASS: zip_codes")


def test_json_file():
    with open('resources.json', 'r') as f:
        data = json.load(f)
    assert 'resources' in data, "JSON should have 'resources' key"
    assert isinstance(data['resources'], list), "Resources should be a list"
    print("PASS: json_file")


# Run all tests
tests = [
    test_load_resources,
    test_required_keys,
    test_languages_are_lists,
    test_categories_exist,
    test_filter_by_category,
    test_search_by_name,
    test_search_case_insensitive,
    test_filter_by_language,
    test_zip_codes,
    test_json_file,
]

passed = 0
failed = 0

for test in tests:
    try:
        test()
        passed += 1
    except AssertionError as e:
        print(f"FAIL: {test.__name__} - {e}")
        failed += 1

print(f"\nResults: {passed} passed, {failed} failed out of {len(tests)} tests")