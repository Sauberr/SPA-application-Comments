# SPA Application: Comments — Technical Requirements

## Description

A Single Page Application for user comments. Users can leave comments that are saved
to a relational database, including user identification data.

---

## Required Technologies

- Object-oriented programming (OOP)
- SQL (PostgreSQL preferred)
- Django + Django ORM
- Vue (preferred), React, or Angular
- Docker
- WebSocket (WS)
- Git

---

## Comment Form Fields

| Field | Type | Required | Rules |
|---|---|---|---|
| User Name | Text | Yes | Latin letters and digits only |
| E-mail | Email | Yes | Valid email format |
| Home page | URL | No | Valid URL format |
| CAPTCHA | Text | Yes | Alphanumeric image challenge |
| Text | Textarea | Yes | All HTML tags forbidden except whitelisted ones |

---

## Main Page Requirements

1. Any comment can receive unlimited nested replies (cascading display).
2. Top-level comments (not replies) are displayed in a table with sorting by:
   - User Name
   - E-mail
   - Date added
   - Each field sortable ascending and descending.
3. Comments are paginated — 25 per page.
4. Protection against XSS attacks and SQL injection.
5. Default sort order — LIFO (newest first).
6. Basic CSS design is required.

---

## File Attachments (JavaScript)

1. Users may attach an image or a text file to a comment.
2. Images must not exceed 320×240 pixels. If larger, proportionally resize to fit. Allowed formats: JPG, GIF, PNG.
3. Text files must not exceed 100 KB. Format: TXT only.
4. File previews must include visual effects (lightbox-style, e.g. Lightbox2).

---

## Allowed HTML Tags (Regex Validation)

Users may use only the following tags in comment text:

```html
<a href="" title=""></a>
<code></code>
<i></i>
<strong></strong>
```

- All other tags must be stripped.
- Tag closing must be validated — output must be valid XHTML.

---

## JavaScript / AJAX Requirements

1. Validation on both client side and server side.
2. Message preview without page reload.
3. Toolbar with tag buttons: `[i]` `[strong]` `[code]` `[a]`.
4. Visual effects and animations are welcome.

---

## Deliverables (All Levels)

| Item | Description |
|---|---|
| Hosting / VDS | Deploy the app so a QA tester can check it via checklist |
| Docker | Package the entire app with all dependencies into a container |
| Git repository | Full commit history for code review |
| README.md | Project description, features, and setup instructions |
| DB schema file | Compatible with MySQL Workbench |
| Demo video | Short recording showing all implemented features |

> Before submitting, run your project from scratch following your own README to verify it works.

---

## Junior+ Level (add to base)

- **Queue** — async task queue (e.g. Celery)
- **Cache** — caching layer (e.g. Redis)
- **Events** — event/signal system (e.g. Django signals)
- **JWT** — token-based authentication

---

## Middle Level (add to Junior+)

- **GraphQL** — query and mutation API
- **Message broker** — RabbitMQ or Kafka
- **NoSQL** — Elasticsearch (preferred), Redis, or MongoDB
- **Cloud** — Azure, AWS, GCP, Yandex Cloud, or any cloud platform

---

## Middle+ Level (add to Middle)

Target load: **1,000,000 messages, 100,000 users within 24 hours**

- Architecture designed to handle the target load
- Load testing suite (e.g. Locust or k6)