-- PL/SQL Blocks with Basic Programming Constructs
-- This file demonstrates sequential statements and unconstrained loops

-- Example 1: Sequential Statements
-- This block shows how statements execute in sequence
DECLARE
    v_number1 NUMBER := 10;
    v_number2 NUMBER := 20;
    v_result NUMBER;
    v_message VARCHAR2(100);
BEGIN
    -- Sequential Statement 1: Addition
    v_result := v_number1 + v_number2;
    DBMS_OUTPUT.PUT_LINE('Addition Result: ' || v_result);
    
    -- Sequential Statement 2: Multiplication
    v_result := v_number1 * v_number2;
    DBMS_OUTPUT.PUT_LINE('Multiplication Result: ' || v_result);
    
    -- Sequential Statement 3: String concatenation
    v_message := 'The numbers were ' || v_number1 || ' and ' || v_number2;
    DBMS_OUTPUT.PUT_LINE(v_message);
    
    -- Sequential Statement 4: Update variable and display
    v_number1 := v_number1 + 5;
    DBMS_OUTPUT.PUT_LINE('Updated first number: ' || v_number1);
END;
/

-- Example 2: Unconstrained Loop (Simple Loop)
-- This block demonstrates an unconstrained loop with EXIT condition
DECLARE
    v_counter NUMBER := 1;
    v_sum NUMBER := 0;
BEGIN
    DBMS_OUTPUT.PUT_LINE('=== Unconstrained Loop Example ===');
    
    -- Simple Loop (unconstrained - runs indefinitely until explicitly exited)
    LOOP
        -- Add current counter to sum
        v_sum := v_sum + v_counter;
        DBMS_OUTPUT.PUT_LINE('Counter: ' || v_counter || ', Sum: ' || v_sum);
        
        -- Exit condition: stop when counter reaches 5
        IF v_counter >= 5 THEN
            EXIT;
        END IF;
        
        -- Increment counter
        v_counter := v_counter + 1;
    END LOOP;
    
    DBMS_OUTPUT.PUT_LINE('Final Sum: ' || v_sum);
END;
/

-- Example 3: Unconstrained Loop with EXIT WHEN
-- Alternative syntax for exiting the loop
DECLARE
    v_num NUMBER := 1;
    v_factorial NUMBER := 1;
BEGIN
    DBMS_OUTPUT.PUT_LINE('=== Factorial Calculation Using Unconstrained Loop ===');
    
    LOOP
        -- Calculate factorial
        v_factorial := v_factorial * v_num;
        DBMS_OUTPUT.PUT_LINE(v_num || '! = ' || v_factorial);
        
        -- Exit when v_num reaches 6
        EXIT WHEN v_num >= 6;
        
        -- Increment number
        v_num := v_num + 1;
    END LOOP;
END;
/

-- Example 4: Combined Sequential Statements and Unconstrained Loop
DECLARE
    v_total NUMBER := 0;
    v_average NUMBER;
    v_count NUMBER := 0;
    v_current NUMBER;
BEGIN
    DBMS_OUTPUT.PUT_LINE('=== Sequential + Loop Constructs ===');
    
    -- Sequential: Initialize with some values
    DBMS_OUTPUT.PUT_LINE('Starting calculation...');
    
    -- Unconstrained loop to process numbers
    LOOP
        -- Generate a random number between 1 and 100
        v_current := ROUND(DBMS_RANDOM.VALUE(1, 100));
        
        -- Add to total and increment count
        v_total := v_total + v_current;
        v_count := v_count + 1;
        
        DBMS_OUTPUT.PUT_LINE('Number ' || v_count || ': ' || v_current);
        
        -- Exit when we have 5 numbers
        EXIT WHEN v_count >= 5;
    END LOOP;
    
    -- Sequential: Calculate average
    v_average := v_total / v_count;
    
    -- Sequential: Display results
    DBMS_OUTPUT.PUT_LINE('Total: ' || v_total);
    DBMS_OUTPUT.PUT_LINE('Count: ' || v_count);
    DBMS_OUTPUT.PUT_LINE('Average: ' || v_average);
END;
/

-- Example 5: Nested Sequential Statements within Loop
DECLARE
    v_outer_counter NUMBER := 1;
BEGIN
    DBMS_OUTPUT.PUT_LINE('=== Nested Sequential Statements ===');
    
    LOOP
        -- Sequential statements inside the loop
        DBMS_OUTPUT.PUT_LINE('Outer Loop Iteration: ' || v_outer_counter);
        
        -- Sequential calculation
        DECLARE
            v_inner_sum NUMBER := 0;
            v_inner_counter NUMBER;
        BEGIN
            -- Inner sequential statements
            v_inner_counter := v_outer_counter * 2;
            v_inner_sum := v_inner_counter + 10;
            
            DBMS_OUTPUT.PUT_LINE('  Inner calculation: ' || v_inner_counter || ' + 10 = ' || v_inner_sum);
        END;
        
        -- Exit condition
        EXIT WHEN v_outer_counter >= 3;
        
        -- Sequential: increment counter
        v_outer_counter := v_outer_counter + 1;
    END LOOP;
END;
/

-- To run these examples, use the following command in SQL*Plus or SQL Developer:
-- SET SERVEROUTPUT ON;
-- Then execute the script: @plsql_basic_constructs.sql