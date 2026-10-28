# Canonical salon content model

The three public pages are served by the `website` app. Its `Category` and
`Hairstyle` models are the canonical source for the public Home portraits,
Our Work carousel, and gallery. `DirectionStep` remains the source for the
How to Find Us route instructions.

The older `studio.Hairstyle` and `studio.StyleImage` models are retained for
database compatibility; they are no longer registered as a second hairstyle
editor in Django Admin and are not queried by the public pages. They contain
seeded external sample-image URLs, so they must not be copied into the live
portfolio blindly: the owner should review and re-add genuine salon work in
the canonical website admin before any legacy content is published.

The old `/studio/` route redirects to Home and old `/studio/style/<slug>/`
links redirect to Our Work. Canonical public routes are:

- `/` — Home
- `/our-work/` — Our Work
- `/find-us/` — How to Find Us
- `/admin/` — Django Admin

Public portfolio images must be uploaded by the owner through Django Admin. The
public views exclude records with no uploaded image, so empty uploads cannot
break a page and external stock images are not accidentally presented as salon work. The new `SiteConfiguration` record in Django Admin controls the public salon name,
tagline, hero copy, Home background, booking URL, address, map embed, and map link.
These fields intentionally start blank until the owner supplies real values.
