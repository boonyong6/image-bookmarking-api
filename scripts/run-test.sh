#!/bin/bash
coverage run --source='.' manage.py test --failfast --shuffle --keepdb --noinput -- accounts && coverage html && coverage xml
