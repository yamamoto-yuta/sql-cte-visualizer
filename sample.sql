WITH
    temp AS (
        SELECT
            1 AS id,
            'a' AS name
        UNION ALL
        SELECT
            2 AS id,
            'b' AS name
    ),

    temp2 AS (
        SELECT
            1 AS id,
            'a' AS name
        UNION ALL
        SELECT
            2 AS id,
            'b' AS name
    ),

    final AS (
        SELECT
            *
        FROM
            temp
        UNION ALL
        SELECT
            *
        FROM
            temp2
    )

SELECT * FROM final
