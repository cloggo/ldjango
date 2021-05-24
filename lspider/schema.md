## Database Schema

### Raw Data

[name, link, slug, tags, quote]

### Design

* link type table
[link_type]

* author table, unique index author
[author]

* author-slug
[author_pk, slug]

* tag table, unique index tag
[tag]

* author link
[author_pk, link_type_pk, link]

* quote, unique index quote
[author_pk, created_at, updated_at, quote]

* quote status
[quote_pk, created_at, status]

* quote tag
[tag_pk, quote_pk]
