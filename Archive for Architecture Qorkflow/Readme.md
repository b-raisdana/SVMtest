# مرحله دوم – طراحی (Story to Task)

این مرحله توسط طراح (دولاپر) طراحی می شود.
خروجی این مرحله یک فایل doc یا هر فرمتی که در confluence راحت نگهداری می شود.


> Crontab: {minute: str = '*', hour: str = '*', day_of_week: str = '*', day_of_month: str = '*', month_of_year:
> str = '*' }

+ /RabbitMQ/Scheduler/scheduled_task_result_publisher(uri: str, parameters: str(JSON({name: str -> value: Any})),
  requester_id: uuid, scheduler_signature: str(MD5))
+ Scheduler/restore_tasks()

# Required Documentations

این عناوینیست که در مستند همراه ریلیز باید به صورت Markdown همراه کد داخل فایل READMNE.md در روت پروژه نگهداری بشود.

تأیید کننده ریلیز موظف است به روز بودن مستند را هم همراه با کد تأیید نماید.

در هر ریلیز نگارش همان ریلیز چسبیده به کد دیده می شود.

# Schedular

یک سیستم اسکجولر که بتواند حالت های بسیار فلکسیبلی از تقویم زمانبندی را ایجاد نماید. زمانبندیهای مورد نظر شامل:

- هر 10 روز و 3 ساعت یک بار
- پنجشنبه ها ساعت 17:00
- شنبه ها ساعت 4:00
- روز سوم هر ماه (تاریخ 3) و ساعت 15:00
- ترکیب این موارد با هم

اسکجولر لازم است قادر باشد در یک زمان از قبل تعیین شده، با فاصله زمانی حداکثر یک سال، یک وظیفه محوله را اجرا نماید.
وظیفه در قالب یک فانکشن یا API است که لازم است به صورت پارامتریک و با قابلیت ارسال پارامترهای متغیر فانکشن یا API برای
اسکجولر قابل تعریف کردن باشد.

قابلیت لازم است به نحوی پیاده سازی شود که برای سرویس های موجود مبتنی بر Python و C++ و C# قابل استفاده باشد. قابلیت لازم
است در ساده ترین حالت ممکن در سرویس های موجود قابل استفاده باشد.

ایجاد یک کانال دسترسی به سرویس که در تمامی پلتفرمهای استفاده کننده قابل استفاده باشد، مانند Message Queue یا API یا ...
قابل استفاده است.

وظایف اسکجول شده لازم است در صورت فیل شدن داکر و بازیابی خودکار توسط اینفرااستراکچر داکر/کوبرنتیز به صورت خودکار بازیابی
گردد.

# Installation and Getting Started Guide

## Python

### add to requirements

add this to your requirements.txt:

```
--index-url https://__token__:REWeDhWKMU3mo6a1Vy3d@https://repo.behinrahkar.com/api/v4/projects/31/packages/pypi/simple
br_sdk
```

### using pip

```
pip install br_sdk --index-url https://__token__:REWeDhWKMU3mo6a1Vy3d@repo.behinrahkar.com/api/v4/projects/31/packages/pypi/simple
```

### importing

import the library inside your ```example.py```:

```python
import br_sdk.Scheduler
```

h3: ### create schedular handle
```python
from br_sdk.Scheduler import Schedular

schedualr = new Schedular(uri='111.111.111.111')
```

# Usage
## Python
### Schedule a task by API
### br_sdk.Scheduler.add_task

schedule task through REST API

```python
from br_sdk.Scheduler import Schedule, Crontab, task, TaskMthods
from datetime import timedelta

task(
    uri='https://example.com/api/1.0.0/delete_user_transient_data',
    parameters={
        'user_id': '012345679abcdef012345679abcdef',
    },
    method=TaskMthods.GET,
    schedule=[
        # - هر 10 روز و 3 ساعت یک بار
        Crontab(timedelta=timedelta(days=10, hours=3)),
        # - پنجشنبه ها ساعت 17:00 
        Crontab(day_of_week=3, hour=17),
        # - شنبه ها ساعت 4:00 
        Crontab(day_of_week=5, hour=4),
        # - روز سوم هر ماه (تاریخ 3) و ساعت 15:00
        Crontab(day_of_month=3, hour=15),
    ],
    requester_id: 'abcdef012345679abcdef012345679',
requester_signature: '703862f5d0ee949ef9fc97c4be2dc6f5',
)
```

in the above example we are creating ...

# Data Types

### Schedule

```python
class br_sdk.Scheduler.Schedule(
parameter: [float, List[float], Crontab, List[Crontab]]

)
```

Examples:

```python
seconds as an
integer, a
timedelta, or a
crontab
from br_sdk.Scheduler import Schedule, Crontab

schedule1 = Schedule(10.5)  # every 10.5 seconds
schedule1 = Schedule([11, 2563])  # every 11 seconds, and every 2563 seconds
schedule1 = Schedule(Crontab(...))  # singular Crontab
schedule1 = Schedule(Crontab(...))  # singular Crontab
schedule2 = Schedule([Crontab(...), Crontab(...), Crontab(...)])  # combination of Crontabs
```

Here's the adjusted documentation with all subheadings under the `### Crontab` heading:

### Crontab

This documentation provides a clear and concise reference for configuring the `Crontab` schedule in `br_sdk.Scheduler`,
with examples demonstrating common use cases.

```python
class br_sdk.Scheduler.Crontab(
minute: str = '*', hour

: str = '*', day_of_week: str = '*', day_of_month: str = '*', month_of_year: str = '*'
)
```

#### Parameters

* minute

    * **Description**: A (list of) integers from 0-59 that represent the minutes of an hour when execution should occur;
      or
      a string representing a Crontab pattern.
    * **Type**: `str` or `list[int]`
    * **Default**: `'*'`
    * **Examples**:
        * `minute='*/15'` (every quarter-hour)
        * `minute='1,13,30-45,50-59/2'` (at minute 1, 13, every minute from 30 to 45, and every 2 minutes from 50 to 59)

* hour

    * **Description**: A (list of) integers from 0-23 that represent the hours of a day when execution should occur; or
      a
      string representing a Crontab pattern.
    * **Type**: `str` or `list[int]`
    * **Default**: `'*'`
    * **Examples**:
        * `hour='*/3'` (every three hours)
        * `hour='0,8-17/2'` (at midnight, and every two hours during office hours)

* day_of_week

    * **Description**: A (list of) integers from 0-6, where Sunday = 0 and Saturday = 6, that represent the days of a
      week
      when execution should occur; or a string representing a Crontab pattern.
    * **Type**: `str` or `list[int]`
    * **Default**: `'*'`
    * **Examples**:
        * `day_of_week='mon-fri'` (weekdays only)
        * `day_of_week='*/2'` (every day that is divisible by two)

* day_of_month
    * **Description**: A (list of) integers from 1-31 that represent the days of the month when execution should occur;
      or a
      string representing a Crontab pattern.
    * **Type**: `str` or `list[int]`
    * **Default**: `'*'`
    * **Examples**:
        * `day_of_month='2-30/2'` (every even-numbered day)
        * `day_of_month='1-7,15-21'` (the first and third weeks of the month)

* month_of_year
    * **Description**: A (list of) integers from 1-12 that represent the months of the year during which execution can
      occur; or a string representing a Crontab pattern.
    * **Type**: `str` or `list[int]`
    * **Default**: `'*'`
    * **Examples**:
        * `month_of_year='*/3'` (the first month of every quarter)
        * `month_of_year='2-12/2'` (every even-numbered month)

#### Examples

Run a Task Every 10 Days at Midnight

```python
from br_sdk.Scheduler import Crontab

crontab_schedule = Crontab(
    minute='0',
    hour='0',
    day_of_month='*/10'
)
```

Run a Task Every Monday at 9 AM

```python
from br_sdk.Scheduler import Crontab

crontab_schedule = Crontab(
    minute='0',
    hour='9',
    day_of_week='1'
)
```

Run a Task on the 1st and 15th of Every Month at Noon

```python
from br_sdk.Scheduler import Crontab

crontab_schedule = Crontab(
    minute='0',
    hour='12',
    day_of_month='1,15'
)
```

Run a Task Every January 1st at Midnight

```python
from br_sdk.Scheduler import Crontab

crontab_schedule = Crontab(
    minute='0',
    hour='0',
    day_of_month='1',
    month_of_year='1'
)
```

# معماری پیاده سازی

![SampleDrawing.drawio.3.drawio.png](SampleDrawing.drawio.3.drawio.png)
این فایل گرافیکی از نوع PNGاست اما در draw.io به شکل جالبی قابل مودیفای کردن است.

این فایل با Google Docs و REAME.md و GitHub و Confluence و ... به خوبی اینگریت می شود.

# Contributor Guidelines

# Code of Conduct

# API Documentation

# Release Notes

# Upgrade plan

#      