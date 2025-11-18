# Address Book Backend (Django)

This project implements a simple backend service for an address(contact) book application, by using **Django** and  **relational database** (SQLite by default)
.

A contact contains fields such as `name`, `email`, and `phone`.  
Contacts can be organized using **labels**, and a contact may have **multiple labels**.

The app provides:
- Create/Delete/List for contacts and labels
- Add/remove labels for contacts
- List: Filter contact by labels
- List: Filter contact by labels and only return email-addresses
- Includes automated tests and documentation

---

##  Setup & Preparation

### 1. Create a virtual environment
```bash
python -m venv your_name_of_env
```

### 2. Activate virtual envrionment

**Windows**
```bash
your_name_of_env\Scripts\activate
```
**Linux**
```bash
source your_name_of_env/bin/activate
```
### 3. Install dependencies
```bash
pip install -r req.txt
```

### 4. Prepare database
```bash
python manage.py makemigrations
python manage.py migrate
```

## Test and Debug

### Auto Test
Automated test covers:

- Creating\Deleting\Listing contacts and labels

- Adding/removing labels to contact

- Listing contacts by labels as filter

- Listing contacts by labels as filter and return only email addresses

```bash
python manage.py test contactbook
```

All tests should pass.

### Run the Server for Manual Testing
```bash
python manage.py runserver 0.0.0.0:8000
```

And open http://127.0.0.1:8000/contactbook/test and click the buttons to test manually, with breakpoints in your IDE.

## Other fun things to implement(yet not):

- Add paging to filtering just in case we don't need all of the data every time.
- Add caching if the contact book is huge.
- Apply ElasticSearch or other apporaches if the contact book is bigger than huge.
- When deleting things, fake the delete first and perform the deletion using a timed task, just in case things are deleted by accident.
