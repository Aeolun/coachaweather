Weather Control
===============

Description
-----------
I'd been wanting to build something like this for a while. It's a weather simulator based on a few small rules that work together to create a complex simulation.

It's not nearly as interesting as I'd hoped it would be (yet), but I didn't have a lot of time to tweak the parameters. I wanted to add some other components like 'vegetation' and making rain and cloud movement dependent on elevation as well.

Install
-------

This project uses `pipenv` to manage the environment in which it runs. Running `pipenv install` should install all the packages you need.

Afterwards, run `python manage.py migrate` to set up the database.

To initialize the base data necessary to run the app easily, run `python manage.py loaddata tile`.

Running
-------
You can run the project by calling `python manage.py runserver 0.0.0.0:8000`. If you run it on your local host, you can change the `0.0.0.0` to `127.0.0.1` to be more secure.

Tests
-----
Run the included tests by calling `python manage.py test`.

Development Comments
--------------------

- Using div's for the map was not the best idea. It severely restricts the amount of data that can be displayed. It would be a better idea to use a canvas here, but for time restrictions.
- No security, but yeah, I don't think I really mind if someone accesses my weather API
- 4 hours spent. Maybe this is slightly more complex than I expected.
- My REST strategy has broken down a bit.
- 8 hours spent. Yeah, slightly too ambitious to fit it in 8 hours... still need some rules to actually see weather in action.
- Shouldn't have made the processor dependent on the Map model, not really nice for testing.
