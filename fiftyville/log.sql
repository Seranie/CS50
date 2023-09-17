-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Look at duck theft case in case report
SELECT *
FROM crime_scene_reports
WHERE description LIKE '%cs50%' ;
-- Crime happened at 1015

--Look up interviews related to duck crime
SELECT *
FROM interviews
WHERE year = 2021
    AND month = 7
    AND day = 28
    AND transcript LIKE '%bakery%';

    -- Thief left bakery parking lot (RUTH)
    -- was at ATM on Leggett Street (EUGENE)
    -- Call (less than a minute) to leave earliest flight out of fiftyville tmr (29 july), ask other person on phone to get ticket (RAYMOND)


-- Check security footage
SELECT *
    FROM bakery_security_logs
    WHERE year = 2021
    AND month = 7
    AND day = 28
    AND minute BETWEEN 15 AND 25
    AND hour = 10;
    -- 8 different license plate found

SELECT *
    FROM atm_transactions
    WHERE atm_location = 'Leggett Street'
        AND year = 2021
        AND month = 7
        AND day = 28
        AND transaction_type = 'withdraw';

-- 8 different accounts found

SELECT *
FROM phone_calls
WHERE year = 2021
    AND month = 7
    AND day = 28
    AND duration <= 60;




-- Find out who has been at the bakery (based on license plate) AND withdrew money from the leggett street ATM on the same day AND made a call that lasted less than a minute
SELECT *
FROM people
    JOIN bank_accounts
        ON people.id = bank_accounts.person_id
    JOIN bakery_security_logs
        ON bakery_security_logs.license_plate = people.license_plate
WHERE account_number
    IN  (SELECT account_number
        FROM atm_transactions
        WHERE atm_location = 'Leggett Street'
            AND year = 2021
            AND month = 7
            AND day = 28
            AND transaction_type = 'withdraw')
    AND people.license_plate
        IN    (SELECT license_plate
                FROM bakery_security_logs
                WHERE year = 2021
                    AND month = 7
                    AND day = 28
                    AND minute BETWEEN 15 AND 25
                    AND hour = 10)
    AND phone_number
        IN (SELECT caller
                FROM phone_calls
                WHERE year = 2021
                    AND month = 7
                    AND day = 28
                    AND duration <= 60);

-- 2 different persons found

-- find fiftyville airports id
SELECT *
FROM airports
WHERE city = 'Fiftyville';

-- id is 8

-- find flight IDs (DESTINATION) based on persons passport number
SELECT *
FROM passengers
WHERE passengers.passport_number IN
    (SELECT passport_number
    FROM people
        JOIN bank_accounts
            ON people.id = bank_accounts.person_id
        JOIN bakery_security_logs
            ON bakery_security_logs.license_plate = people.license_plate
    WHERE account_number
        IN  (SELECT account_number
            FROM atm_transactions
            WHERE atm_location = 'Leggett Street'
                AND year = 2021
                AND month = 7
                AND day = 28
                AND transaction_type = 'withdraw')
        AND people.license_plate
            IN    (SELECT license_plate
                    FROM bakery_security_logs
                    WHERE year = 2021
                        AND month = 7
                        AND day = 28
                        AND minute BETWEEN 15 AND 25
                        AND hour = 10)
        AND phone_number
            IN (SELECT caller
                    FROM phone_calls
                    WHERE year = 2021
                        AND month = 7
                        AND day = 28
                        AND duration <= 60)
);

-- FOUND 4 flights, 3 from the same person

-- find EARLIEST flights from fiftyville, using the ids that corresponds to the found flights.

SELECT *
FROM flights
WHERE id IN
    (SELECT flight_id
    FROM passengers
    WHERE passengers.passport_number IN
        (SELECT passport_number
        FROM people
            JOIN bank_accounts
                ON people.id = bank_accounts.person_id
            JOIN bakery_security_logs
                ON bakery_security_logs.license_plate = people.license_plate
        WHERE account_number
            IN  (SELECT account_number
                FROM atm_transactions
                WHERE atm_location = 'Leggett Street'
                    AND year = 2021
                    AND month = 7
                    AND day = 28
                    AND transaction_type = 'withdraw')
            AND people.license_plate
                IN    (SELECT license_plate
                        FROM bakery_security_logs
                        WHERE year = 2021
                            AND month = 7
                            AND day = 28
                            AND minute BETWEEN 15 AND 25
                            AND hour = 10)
            AND phone_number
                IN (SELECT caller
                        FROM phone_calls
                        WHERE year = 2021
                            AND month = 7
                            AND day = 28
                            AND duration <= 60)
    ))
    AND day = 29
    AND origin_airport_id = 8
    ORDER BY hour ASC
    LIMIT 1;

-- 1 flights found leaving fiftyville, headed to id 4

-- CULPRITS DETAILS
SELECT *
FROM people
WHERE passport_number = 5773159633;

-- CULPRITS DESTINATION
SELECT *
FROM airports
WHERE id = 4;

-- FIND ACCOMPLICE NUMBER
SELECT *
FROM phone_calls
WHERE caller IN
    (SELECT phone_number
    FROM people
    WHERE passport_number = 5773159633)
    AND day = 28
    AND duration <= 60;


-- FIND ACCOMPLICE DETAILS
SELECT *
FROM people
WHERE phone_number IN
    (
        SELECT receiver
        FROM phone_calls
        WHERE caller IN
            (SELECT phone_number
            FROM people
            WHERE passport_number = 5773159633)
            AND day = 28
            AND duration <= 60);
