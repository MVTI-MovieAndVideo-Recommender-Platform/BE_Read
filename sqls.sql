SHOW DATABASES;

Create database content;

use content;

CREATE TABLE media (
    id INT UNSIGNED PRIMARY KEY,
    type ENUM('movie', 'series') NOT NULL,
    title VARCHAR(255) NOT NULL,
    runtime SMALLINT UNSIGNED NOT NULL,
    release_date DATE NOT NULL,
    certification VARCHAR(255) DEFAULT NULL,
    genre VARCHAR(255) NOT NULL,
    origin_country VARCHAR(255) NOT NULL,
    overview VARCHAR(2000) NOT NULL,
    director VARCHAR(255) DEFAULT NULL,
    actor VARCHAR(1000) DEFAULT NULL,
    platform VARCHAR(255) NOT NULL,
    rating_value FLOAT NOT NULL,
    rating_count INT UNSIGNED NOT NULL,
    posterurl_count TINYINT UNSIGNED DEFAULT 0,
    backdropurl_count TINYINT UNSIGNED DEFAULT 0,
    posterurl VARCHAR(1000) DEFAULT NULL,
    backdropurl VARCHAR(1000) DEFAULT NULL
);

CREATE TABLE id_manager (
    next_movie_id INT DEFAULT 1,
    next_series_id INT DEFAULT 2
);

CREATE TABLE crawl_date (
    start_date DATE DEFAULT "2024-06-06",
    end_date DATE
)

INSERT INTO id_manager VALUES (1, 2);

use content;

CREATE PROCEDURE insert_media(IN media_type ENUM('movie', 'series'),
IN title VARCHAR(255),
IN runtime SMALLINT UNSIGNED,
IN release_date DATETIME,
IN certification VARCHAR(255),
IN genre VARCHAR(255),
IN origin_country VARCHAR(255),
IN overview VARCHAR(2000),
IN director VARCHAR(255),
IN actor VARCHAR(1000),
IN platform VARCHAR(255),
IN rating_value FLOAT,
IN rating_count INT UNSIGNED,
IN posterurl_count TINYINT UNSIGNED,
IN backdropurl_count TINYINT UNSIGNED,
IN posterurl VARCHAR(1000),
IN backdropurl VARCHAR(1000))
BEGIN
    DECLARE new_id INT;

    IF media_type = 'movie' THEN
        SELECT next_movie_id INTO new_id FROM id_manager;
        INSERT INTO media (id,type,title,runtime, release_date,
        certification,
        genre,
        origin_country,
        overview,
        director,
        actor,
        platform,
        rating_value,
        rating_count,
        posterurl_count,
        backdropurl_count,
        posterurl,
        backdropurl) VALUES (new_id,media_type,title,runtime, release_date,
        certification,
        genre,
        origin_country,
        overview,
        director,
        actor,
        platform,
        rating_value,
        rating_count,
        posterurl_count,
        backdropurl_count,
        posterurl,
        backdropurl);
        UPDATE id_manager SET next_movie_id = next_movie_id + 2;
    ELSEIF media_type = 'series' THEN
        SELECT next_series_id INTO new_id FROM id_manager;
        INSERT INTO media (id,type,title,runtime,release_date,
        certification,
        genre,
        origin_country,
        overview,
        director,
        actor,
        platform,
        rating_value,
        rating_count,
        posterurl_count,
        backdropurl_count,
        posterurl,
        backdropurl) VALUES (new_id, media_type, title, runtime, release_date,
        certification,
        genre,
        origin_country,
        overview,
        director,
        actor,
        platform,
        rating_value,
        rating_count,
        posterurl_count,
        backdropurl_count,
        posterurl,
        backdropurl);
        UPDATE id_manager SET next_series_id = next_series_id + 2;
    END IF;
END;

use content;

CALL insert_media (
    'series',
    '키다리 아저씨',
    '1990-01-14',
    0,
    '전체',
    '코미디, 애니메이션, 드라마',
    '일본',
    "고아이지만 언제나 밝은 주디와 그런 주디를 도와주는 후견인 '키다리 아저씨' 의 사랑 이야기를 그린 애니메이션",
    '',
    'Mitsuko Horie,
島田敏,
佐藤智恵,
田中秀幸,
天野由梨,
Hiromi Tsuru,
Hiroshi Masuoka,
京田尚子,
緒方賢一,
勝生真沙子,
Michitaka Kobayashi,
Tatsukou Ishimori',
    'wavve, watcha, tving',
    4.2,
    1623,
    5,
    3,
    'https://image.tmdb.org/t/p/original/2L7IZ1mtXFotV3HtwEoy7mpYxom.jpg, https://image.tmdb.org/t/p/original/4XUuwLIy3YD3AesTN9xBjWG9miH.jpg, https://image.tmdb.org/t/p/original/rMTIvk36wuOCTkGgiBchpFOxb3y.jpg, https://image.tmdb.org/t/p/original/zef8q6wOFXHlKKc709oasldbkGG.jpg, https://image.tmdb.org/t/p/original/xETbNLfW4XWX7v5ZfFmiT6QCgRg.jpg
',
    'https://image.tmdb.org/t/p/original/6ve31bSQjlYT9wEYt3DDxzj1uvh.jpg, https://image.tmdb.org/t/p/original/ekei3HikUTydvWGdbt0D5Tyn2cX.jpg, https://image.tmdb.org/t
    /p/original/eLdxojliLvlgJvsWCjNBUZDMgKa.jpg
'
);

GRANT
SELECT, RELOAD,
SHOW DATABASES, REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'admin' @'%';

FLUSH PRIVILEGES;