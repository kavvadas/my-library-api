/* users (id, name, email, created_at)
products (id, name, category, price, stock)
orders (id, user_id, created_at, total_amount)
order_items (id, order_id, product_id, quantity, unit_price) */

/* Assumptions: 
    -PostgreSQL
    -The 'created_at' fields are of type DATE
    -The 'total_amount' field in the 'orders' table is calculated as the sum of (quantity * unit_price) for all items in the order
     */

/*1. Top 5 χρήστες με τα περισσότερα έσοδα τους τελευταίους 3 μήνες*/
/* Αυτό το ερώτημα επιλέγει τους κορυφαίους 5 χρήστες με τα περισσότερα έσοδα από παραγγελίες που έχουν γίνει τους τελευταίους 3 μήνες. 
Χρησιμοποιεί ένα JOIN για να συνδέσει τους πίνακες 'users' και 'orders' με βάση το user_id, 
φιλτράρει τις παραγγελίες που έχουν δημιουργηθεί τους τελευταίους 3 μήνες και κάνει aggregation των εσόδων,
επιστρέφοντας τους 5 χρήστες με τα περισσότερα έσοδα χρησιμοποιώντας την συνάρτηση LIMIT. */
SELECT
    u.id,
    u.name,
    u.email,
    o.total_amount as total_revenue
FROM users u
JOIN orders o
    ON u.id = o.user_id
WHERE o.created_at >= CURRENT_DATE - INTERVAL '3 months'
GROUP BY
    u.id,
    u.name,
    u.email,
    total_revenue
ORDER BY total_revenue DESC
LIMIT 5;

/*1. Προϊόντα που δεν έχουν αγοραστεί ποτέ*/
/* Αυτό το ερώτημα επιλέγει όλα τα προϊόντα που δεν έχουν αγοραστεί ποτέ. 
Χρησιμοποιεί ένα LEFT JOIN για να συνδέσει τον πίνακα 'products' με τον πίνακα 'order_items' με βάση το product_id, 
και φιλτράρει τα αποτελέσματα για να επιστρέψει μόνο τα προϊόντα που δεν έχουν αντιστοιχιστεί σε καμία παραγγελία (δηλαδή, όπου το order_id είναι NULL). */
SELECT
    p.*
FROM products p
LEFT JOIN order_items oi
    ON p.id = oi.product_id
WHERE oi.order_id IS NULL;

/*1. Μηνιαίο revenue ανά κατηγορία (τελευταίοι 6 μήνες) — με window function*/
/* Αυτό το ερώτημα υπολογίζει το μηνιαίο revenue ανά κατηγορία για τους τελευταίους 6 μήνες.
Χρησιμοποιεί ένα JOIN για να συνδέσει τους πίνακες 'products', 'order_items' και 'orders' με βάση τα product_id και order_id,
φιλτράρει τις παραγγελίες που έχουν δημιουργηθεί τους τελευταίους 6 μήνες, και κάνει aggregation των εσόδων ανά κατηγορία και μήνα.
Στη συνέχεια, χρησιμοποιεί μια window function για να υπολογίσει το συνολικό revenue ανά κατηγορία. 
Το window function που χρησιμοποιείται είναι το SUM() OVER (PARTITION BY p.category). */
SELECT
    p.category,
    DATE_TRUNC('month', o.created_at) AS month,
    SUM(oi.quantity * oi.unit_price) AS monthly_revenue,
    SUM(SUM(oi.quantity * oi.unit_price)) OVER (PARTITION BY p.category) AS total_revenue_per_category
FROM products p
JOIN order_items oi
    ON p.id = oi.product_id
JOIN orders o
    ON oi.order_id = o.id
WHERE o.created_at >= CURRENT_DATE - INTERVAL '6 months'
GROUP BY
    p.category,
    month
ORDER BY
    p.monthly_revenue DESC;

/*1. Χρήστες που έκαναν order τον Ιανουάριο αλλά όχι τον Φεβρουάριο*/
/* Αυτό το ερώτημα επιλέγει τους χρήστες που έκαναν παραγγελία τον Ιανουάριο αλλά όχι τον Φεβρουάριο.
Χρησιμοποιεί ένα JOIN για να συνδέσει τους πίνακες 'users' και 'orders' με βάση το user_id, 
και φιλτράρει τις παραγγελίες για να βρει τους χρήστες που έκαναν παραγγελία τον Ιανουάριο (EXTRACT(MONTH FROM o.created_at) = 1), 
αλλά όχι τον Φεβρουάριο (EXTRACT(MONTH FROM o.created_at) = 2).*/
SELECT DISTINCT
    u.*
FROM users u
JOIN orders o
    ON u.id = o.user_id
WHERE EXTRACT(MONTH FROM o.created_at) = 1
AND u.id NOT IN (
    SELECT user_id
    FROM orders
    WHERE EXTRACT(MONTH FROM created_at) = 2
);