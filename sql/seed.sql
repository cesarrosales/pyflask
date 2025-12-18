BEGIN;

-- Band
INSERT INTO bands (name)
VALUES ('Hulder')
ON CONFLICT (name) DO NOTHING;

-- Album
INSERT INTO albums (band_id, title, release_year)
SELECT id, 'Verses In Oath', 2024
FROM bands
WHERE name = 'Hulder'
ON CONFLICT (band_id, title) DO NOTHING;

-- Songs
WITH album AS (
    SELECT a.id
    FROM albums a
    JOIN bands b ON b.id = a.band_id
    WHERE b.name = 'Hulder'
      AND a.title = 'Verses In Oath'
)
INSERT INTO songs (album_id, title, lyrics)
SELECT album.id, s.title, s.lyrics
FROM album
CROSS JOIN (
    VALUES
        ('An Elegy', 'Not available'),
        ('Boughs Ablaze', 'Not available'),
        ('Hearken The End', $$Mourning - in wind whipped flesh
Sadness - befalls my heart
Blood falls - as a spring doth flow
The stream of tears must end
I stand with withered soul
Alone in my sorrow
Neath the branches of ancient oak
The stream of tears must end
The will of my kin is met with bereavement
For they can leech not my agony
I've given birth to desires
Yet forever seek tranquility
Descending into whispers once distant and obscure
Clarity is discerned from their tongues
I lust for an unending coldness
And cry to the light of the moon
One with the breeze that rides on the waves
I am the stone that lies underfoot
My whispers shall rustle the dew covered branches
And forever carry my pain
Purified by my own hand
Lead me to the open gate
In endless lament
I Hearken the end$$),
        ('Verses In Oath', 'Not available'),
        ('Lamentation', 'Not available'),
        ('An Offering', 'Not available'),
        ('Cast Into The Well Of Remembrance', 'Not available'),
        ('Vessel Of Suffering', 'Not available'),
        ('Enchanted Steel', 'Not available'),
        ('Veil Of Penitence', 'Not available')
) AS s(title, lyrics)
ON CONFLICT (album_id, title) DO NOTHING;

COMMIT;

-- ============================
-- Verification
-- ============================

-- List all songs for the album
SELECT
    b.name   AS band,
    a.title  AS album,
    s.title  AS song,
    CASE
        WHEN s.lyrics = 'Not available' THEN 'NO LYRICS'
        ELSE 'HAS LYRICS'
    END AS lyrics_status
FROM bands b
JOIN albums a ON a.band_id = b.id
JOIN songs s ON s.album_id = a.id
WHERE b.name = 'Hulder'
  AND a.title = 'Verses In Oath'
ORDER BY s.id;