# Bug Hunt

## Ο παρακάτω κώδικας έχει 3 bugs. Βρες τα και εξήγησέ τα στο αρχείο bugs.md (τι είναι, γιατί είναι πρόβλημα, πώς το διορθώνεις).

```text
@app.get(&quot;/users/{user_id}/orders&quot;)
def get_user_orders(user_id: int, db: Session = Depends(get_db)):
user = db.query(User).filter(User.id == user_id).first()
orders = db.query(Order).all()
result = []
for order in orders:
if order.user_id == user_id:
result.append({
&quot;id&quot;: order.id,
&quot;total&quot;: order.total_amount,
&quot;password&quot;: user.password
})
return result
```
---

### Bug 1 - Έκθεση ευαίσθητων δεδομένων του χρήστη (security bug / data exposure)

"password": user.password 

**Γιατί είναι πρόβλημα;**
* Ποτέ δεν επιστρέφουμε passwords απο API Endpoints γιατί θεωρείται sensitive data
* Δημιουργεί σοβαρό security risk 
* Παραβιάζει βασικές αρχές σχεδίασης APIs

**Πώς διορθώνεται;**
* Απλώς αφαιρούμε το πεδίο, δηλαδή ΔΕΝ επιστρέφουμε το password



### Bug 2 - Μη αποδοτικό query κάνωντας fetch όλων των παραγγελιών (performance bug / full table scan)

orders = db.query(Order).all() 
for order in orders: 
    if order.user_id == user_id:


**Γιατί είναι πρόβλημα;**
* Επιστρέφει **ΟΛΑ** τα records απο την βάση, χωρίς να θέλουμε αυτό
* Δεν χρησιμοποιούνται indexes
* Πολύ κακή απόδοση σε μεγάλα DATASETS

**Πώς διορθώνεται;**
```text
orders = db.query(Order).filter(Order.user_id == user_id).all()
```
* Αυτό επιστρέφει τις **παραγγελίες ανα χρήστη**, καθώς έχουμε **μειώσει κατα πολύ** τα records που επιστρέφονται
* Χρησιμοποιείται **index**, στο user_id



### Bug 3 - Δεν ελέγχεται αν υπάρχει ο χρήστης (runtime bug / NoneType Error)

user = db.query(User).filter(User.id == user_id).first()
Το παραπάνω μπορεί να επιστρέψει None.

Έπειτα χρησιμοποιούμε πεδίου του user:
user.password

> Στην συγκεκριμένη περίπτωση επειδή είναι sensitive data το password,
> θα μπορούσε να χρησιμοποιηθεί άλλο πεδίο του user (πχ. user.first_name)
> το οποίο θα δημιουργόυσε το ίδιο πρόβλημα (Bug 3).

**Γιατί είναι πρόβλημα;**
* Αν ο χρήστης δεν υπάρχει: user = None
* Προκαλεί crash (**AttributeError**)
* Επιστρέφει **500 error** αντί για **404 error** που είναι το σωστό, που σημαίνει λάθος error handling

**Πώς διορθώνεται;**
```text
if not user: 
    raise HTTPException(status_code=404, detail="User not found")
```