# Build a PC Part Picker (Project-PFA-Stack)

Our site is focused on featuring computer hardware and components. Our goal is to provide information to consumers who are in the market for buying new computers or components with the information they need. We hope give more structure to building computer parts and offer recommendations and easily direct users to the components they need. We also hope to provide price statistics on whether it is a good time to buy or simply an historical low.

Link to prototype site: http://bapc.io/

Our project is hosted here: https://github.com/tangjon/PROJECT-PCPARTS

## Frameworks/Languages

### Backend
[Django](https://www.djangoproject.com/) - Python Web Framework

### Database
[SQLite](https://www.sqlite.org/index.html) - SQL Relational database (built into Django by default)

### Front End
[Django Templating](https://docs.djangoproject.com/en/2.0/topics/templates/)

***

Site structure (Rough Road Project Road Map)
- Home
- Login
- User settings and authentication
- Build creation page
- Part browse page, per category basis
- Part detail page (pricing, comments, reviews)
- Part Filter

Project Phase 1: (COMPLETE)
- Backbone design completed (Modelling, views, template return plain unformatted html)
- GPU only but with design accounting for more types of components
- Figure out how to generate list of parts

Project Phase 2: (COMPLETE)
- Add in UI, basic JS functionality
- CSS styling (Twitter Bootstrap)

Project Phase 3: (COMPLETE)
- Finish adding in other types of components aside from GPUs if desired
- Bring project online on VPS

Project Phase 4: (PENDING)
- Integrate Amazon API

manage.py runserver  --settings=bapccanada.settings.local
django-admin runserver --settings=bapccanada.settings.dev


## Contributers

[Gao-Gary](https://github.com/Gao-Gary) - Gary Gao

[tangjon](https://github.com/tangjon) - Jonathan Tang