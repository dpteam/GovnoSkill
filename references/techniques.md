# Арсенал приёмов

64 приёма, из которых собирается говнокод. Каждый — самостоятельная болезнь;
хороший ответ использует 2–4, а не все сразу.

Пометки: **[1–5]** — минимальный уровень, где приём уместен.
**[опасно]** — приём легко превращается в реальный вред, показывай только стиль.

---

## A. Имена

### A1. `data`, `data2`, `data3` **[1]**
```python
data = get_users()
data2 = [x for x in data if x.active]
data3 = data2
```
Зачем: главный герой не назван, зато у него есть нумерованные клоны.

### A2. Имя-эволюция **[1]**
```js
let result = calc();
let result2 = result;
let resultFinal = result2;
let resultFinalFixed = resultFinal;
```
Зачем: видно, что человек боялся удалять — и не удалял.

### A3. Транслит-мутант **[2]**
```php
$kolvoTovarovNaSkladeFinal2 = 0;
$dataPrihod = [];
$tempArrDlyaSortirovki = [];
```
Зачем: три системы письма в одном идентификаторе, и ни одной причины.

### A4. Имя врёт **[3]**
```csharp
public User GetUser(int id)
{
    _db.Users.Remove(id);
    _db.SaveChanges();
    return null;
}
```
Зачем: единственный комментарий в проекте — имя метода, и он лжёт.

### A5. Аббревиатура на шесть букв **[2]**
```java
int clcTtlPrcWthDsc(int a, int b) { ... }
```
Зачем: расшифровку знал только автор. Автор уволился в 2016-м.

### A6. Венгерская нотация в 2026 **[2]**
```csharp
string strName;
int intCount;
bool bIsValid;
List<User> lstUserObjects;
```
Зачем: тип уже в типе, но традиция сильнее.

### A7. Имя = описание типа **[3]**
```ts
const usersObjectListArray: UserObject[] = [];
```
Зачем: `Array` и `List` одновременно, на всякий случай.

### A8. Однобуквенные глобалы **[3]**
```js
var a, b, c, d, e, f, g, q;
function calc() { q = a + b * c - d / e; return q; }
```
Зачем: код компилируется, читатель — нет.

### A9. Файлы-клоны **[1]**
```
utils.js
utils2.js
utils_new.js
utils_final.js
utils (1).js
```
Зачем: история версий, рассказанная именами файлов.

---

## B. Поток управления

### B1. Лестница `if/else` без `return` **[1]**
```js
function check(x) {
  if (x > 0) {
    result = "positive";
  } else {
    if (x < 0) {
      result = "negative";
    } else {
      if (x === 0) {
        result = "zero";
      } else {
        result = "impossible";
      }
    }
  }
  return result;
}
```
Зачем: `else` после `return` — грех, но `else` вместо `return` — стиль жизни.

### B2. `== true` **[1]**
```python
if is_valid == True:
    if not is_deleted == False:
        pass
```
Зачем: булево значение прошло три проверки, чтобы остаться собой.

### B3. Пустой `if` с точкой с запятой **[2]**
```csharp
if (user.IsAdmin);
{
    DeleteEverything();
}
```
Зачем: классика govnokod #28985. Блок выполняется всегда, а IDE красит
точку с запятой серым по серому фону.

### B4. `goto` как цикл **[3]**
```c
int i = 0;
loop:
    printf("%d\n", i++);
    if (i < 10) goto loop;
```
Зачем: `for` не изобрели, зато изобрели метки. [опасно: только демо]

### B5. `while (true)` и `break` на 47-й строке **[3]**
```python
while True:
    row = read()
    if not row:
        break
    if row.startswith("#"):
        continue
    if "error" in row:
        break
    if len(row) > 100:
        break
    process(row)
```
Зачем: условие выхода размазано по функции, как смысл жизни.

### B6. Флаг вместо `return` **[2]**
```java
boolean found = false;
for (User u : users) {
    if (u.getId() == id) {
        found = true;
        current = u;
    }
}
if (found) { return current; }
return null;
```
Зачем: нашли — но продолжили искать, вдруг найдётся ещё раз.

### B7. Двойное отрицание **[2]**
```js
if (!(!isEnabled)) { enable(); }
if (!!value == true) { use(value); }
```
Зачем: `!` — как соль: чем больше, тем хуже.

### B8. `switch` на 40 кейсов **[3]**
```csharp
switch (code) {
  case "11": Console.WriteLine(table[0,0]); break;
  case "12": Console.WriteLine(table[0,1]); break;
  case "13": Console.WriteLine(table[0,2]); break;
  // ... ещё 37 строк, индекс уже очевиден
}
```
Зачем: govnokod #28877. Таблица на 5×5 разложена в 25 `case`.

### B9. `else if` после `return` **[1]**
```js
function f(x) {
  if (x === 1) return "one";
  else if (x === 2) return "two";
  else return "many";
}
```
Зачем: не ошибка, но маркер: человек ещё не встречал линтер.

### B10. Изменение счётчика в теле **[3]**
```c
for (int i = 0; i < n; i++) {
    if (arr[i] == 0) i++;
    if (arr[i] == -1) i += 2;
}
```
Зачем: цикл идёт по массиву, но не туда.

### B11. Рекурсия вместо цикла **[3]**
```python
total = 0
def sum_all(items, i=0):
    global total
    if i < len(items):
        total += items[i]
        sum_all(items, i + 1)
    return total
```
Зачем: стек — тоже память, и его не жалко.

### B12. `for` на одну итерацию **[2]**
```python
for _ in range(1):
    do_the_thing()
```
Зачем: задел на будущее, которое не наступит.

---

## C. Данные и типы

### C1. Всё — строка **[2]**
```python
user_id = "42"
is_active = "true"
deleted_at = "NULL"
age = "17"
if age > 18:            # сравнение строк, но "работает"
    allow()
```
Зачем: типы — для слабаков, строки — для всех.

### C2. Магическое число **[1]**
```js
if (items.length > 17) {          // 17 — потому что так надо
  setTimeout(retry, 3600 * 1000); // час, но лучше в миллисекундах
}
```
Зачем: число знает контекст, но не делится им.

### C3. Булев параметр-переключатель **[3]**
```python
def save(user, True, False, True, None):
    ...
```
Зачем: сигнатура стала загадкой, а IDE подсказывает имена — но не смысл.

### C4. Словарь вместо класса **[3]**
```js
const user = {
  id: 1, name: "x", isAdmin: true, _tmp: null, __cache: {}, get: undefined
};
```
Зачем: структура есть, гарантий нет, опечатки бессмертны.

### C5. Глобал как канал связи **[3]**
```python
current_request = None
current_user = None
current_tenant = None

def handle(req):
    global current_request, current_user, current_tenant
    current_request = req
    current_user = req.user
```
Зачем: передача аргументов — лишняя работа, есть же модуль.

### C6. Мутабельный аргумент по умолчанию **[3]**
```python
def add_tag(tag, tags=[]):
    tags.append(tag)
    return tags
```
Зачем: состояние между вызовами — бесплатно и незаметно.

### C7. Сравнение, которое врёт **[3]**
```js
if (input == 0) { /* [] и "0" тоже подойдут */ }
```
```java
Integer a = 127, b = 127;   // a == b → true
Integer c = 128, d = 128;   // c == d → false
```
Зачем: язык сам решит, что ты имел в виду.

### C8. Дата — строкой **[2]**
```python
date = "12.11.26"
if date > "01.01.25":   # лексикографически, но как-то работает
    expired = True
```
Зачем: ISO 8601 существует ровно для того, чтобы его игнорировали.

### C9. `null` в трёх ролях **[3]**
```java
User find(String id) {
    return null; // не найден
    // или: ошибка БД
    // или: нет прав
    // или: ещё не загружено
}
```
Зачем: одно значение — четыре смысла — ноль информации.

### C10. Параллельные массивы **[4]**
```js
const names = ["a", "b", "c"];
const ages = [20, 30, 40];
const emails = ["a@x", "b@x", "c@x"];
// индекс 2 удалён из names, остальные живут
```
Зачем: объект из трёх полей разложен на три источника рассинхрона.

---

## D. Функции и структура

### D1. God-функция **[3]**
```python
def process():
    # 40 строк валидации
    # 30 строк запросов в БД
    # 20 строк формирования HTML
    # 15 строк отправки почты
    # 10 строк логирования
    # и один print("OK") в конце
```
Зачем: одна функция — один файл — одна жизнь.

### D2. Копипаста с расхождением **[2]**
```python
price = qty * rate
price = qty * rate * 1.2   # вторая копия, уже с НДС
price = qty * rate * 1.2   # третья, но rate уже другой
```
Зачем: три версии правды, и все три «проверены».

### D3. Имя-перечисление обязанностей **[3]**
```java
public String getAndValidateAndSaveUserAndSendEmail(String name) { ... }
```
Зачем: метод назван честно — и это самое страшное.

### D4. Девять параметров **[3]**
```csharp
void Create(string a, string b, string c, int d, int e, bool f, bool g,
            DateTime h, string i = null, string j = null) { }
```
Зачем: объект напрашивался, но объект — это ответственность.

### D5. Побочный эффект в геттере **[3]**
```csharp
public int Count
{
    get { _db.SaveChanges(); return _items.Count; }
}
```
Зачем: чтение свойства меняет базу. Отладчик это обожает.

### D6. `main` как свалка **[2]**
```go
func main() {
    // 700 строк: конфиг, роуты, миграции, бизнес-логика, тестовые данные
}
```
Зачем: точка входа стала точкой невозврата.

### D7. Функция в функции в функции **[3]**
```js
function outer() {
  function inner() {
    function deeper() {
      function why() { return 42; }
      return why();
    }
    return deeper();
  }
  return inner();
}
```
Зачем: замыкания — инструмент, а не способ спрятаться.

### D8. `utils` на 3000 строк **[3]**
```python
# utils.py
def format_date(...): ...
def send_email(...): ...
def calc_tax(...): ...
def resize_image(...): ...
def parse_xml(...): ...
# (ещё 2980 строк, включая три разных format_date)
```
Зачем: свалка с названием «полезное».

### D9. Класс-рекорд с методами **[3]**
```java
class User {
    String a, b, c, d, e, f, g, h;
    void doIt() { ... }
}
```
Зачем: поля есть, модель отсутствует.

### D10. Циклический импорт **[4]**
```python
# a.py
from b import helper
# b.py
from a import helper2
```
Зачем: работает, пока никто не запускает файл напрямую.

---

## E. Ошибки

### E1. Пустой `catch` **[2]**
```java
try {
    save();
} catch (Exception e) {
}
```
Зачем: ошибки — это мнение, а у нас своё.

### E2. `catch` → `null` **[2]**
```csharp
try { return Parse(x); }
catch { return null; }
```
Зачем: сбой превращается в «данных нет» — и живёт так годами.

### E3. `try` на весь `main` **[3]**
```python
def main():
    try:
        everything()
    except:
        print("error")
```
Зачем: обработка ошибок на уровне «что-то пошло не так».

### E4. `except Exception: pass` **[2]**
```python
try:
    do_important()
except Exception:
    pass
```
Зачем: самый популярный способ скрыть баг от себя.

### E5. Два механизма ошибок сразу **[4]**
```c
int rc = do_work();        // -1 при ошибке
if (rc != 0) {
    throw new RuntimeException("rc=" + rc);  // но функция не бросает
}
```
Зачем: код возврата, исключение и лог — три новости об одном.

### E6. `new Exception("Error")` **[1]**
```java
throw new Exception("Error");
```
Зачем: сообщение содержит всё, кроме информации.

### E7. Логи через `print` **[1]**
```python
print("!!! START !!!")
print("user =", user)
print("OK")
print("!!! END !!!")
```
Зачем: observability уровня «здравствуй, консоль».

### E8. Retry без паузы **[4]**
```python
while True:
    try:
        return api.call()
    except:
        continue
```
Зачем: сервис уже лежит, но мы его добиваем.

---

## F. Абстракции

### F1. `AbstractFactoryFactory` **[4]**
```java
public abstract class AbstractUserServiceFactoryProvider { }
public class UserServiceFactoryProviderImpl extends AbstractUserServiceFactoryProvider { }
```
Зачем: один класс — один пользователь — четыре сущности.

### F2. Интерфейс на один класс **[4]**
```csharp
public interface ICalculator { int Add(int a, int b); }
public class Calculator : ICalculator { public int Add(int a, int b) => a + b; }
```
Зачем: «на будущее», которое не наступило за 9 лет.

### F3. Наследование ради строки **[4]**
```python
class BaseRepo: pass
class UserRepo(BaseRepo): pass
class AdminUserRepo(UserRepo): pass   # отличие: один if внутри
```
Зачем: иерархия вместо параметра.

### F4. Суффиксы-пустышки **[3]**
```
UserManager, UserHelper, UserService, UserUtil, UserHandler, UserProcessor
```
Зачем: шесть имён, одна ответственность, ноль границ.

### F5. Стратегия на два случая **[4]**
```ts
interface PaymentStrategy { pay(): void; }
class CardPayment implements PaymentStrategy { ... }
class CashPayment implements PaymentStrategy { ... }
// switch из двух веток был бы 4 строки вместо 40
```
Зачем: паттерн применён, задача — нет.

### F6. DI ради одного объекта **[4]**
```csharp
services.AddSingleton<IClock, Clock>();
services.AddSingleton<IClockProvider, ClockProvider>();
services.AddSingleton<IClockProviderFactory, ClockProviderFactory>();
```
Зачем: `DateTime.Now` был слишком прост.

### F7. Обёртка над обёрткой **[4]**
```python
def get_user(uid):
    return _get_user(uid)

def _get_user(uid):
    return __get_user(uid)

def __get_user(uid):
    return db.fetch(uid)
```
Зачем: слои на всякий случай, все прозрачные.

### F8. `BaseAbstractEntityModel` **[4]**
```python
class BaseAbstractEntityModel(ABC):
    pass
class BaseEntityModel(BaseAbstractEntityModel):
    pass
class User(BaseEntityModel):
    pass
```
Зачем: три уровня, чтобы объявить одно поле.

---

## G. Производительность

### G1. Запрос в цикле **[3]**
```python
for row in rows:
    user = db.query("SELECT * FROM users WHERE id = ?", row.user_id)
    row.user = user
```
Зачем: N+1 — не баг, а архитектурное решение на каждый чих.

### G2. `SELECT *` **[2]**
```sql
SELECT * FROM orders
WHERE created_at > '2020-01-01'
```
Зачем: колонки меняются, отчёт ломается, никто не знает почему.

### G3. Сортировка пузырьком **[2]**
```python
for i in range(len(a)):
    for j in range(len(a) - 1):
        if a[j] > a[j + 1]:
            a[j], a[j + 1] = a[j + 1], a[j]
```
Зачем: на 10 элементах незаметно, на 10 000 — заметно всем.

### G4. `Sleep` как синхронизация **[4]**
```csharp
StartJob();
Thread.Sleep(3000);   // «должно хватить»
CheckResult();
```
Зачем: время — самый надёжный API, особенно на слабой машине.

### G5. Вечный кэш **[4]**
```js
let cache = {};
function getUser(id) {
  if (!cache[id]) cache[id] = api.getUser(id);
  return cache[id];
}
```
Зачем: пользователи меняются, кэш — нет.

### G6. `+=` строк в цикле **[3]**
```java
String html = "";
for (Item i : items) html += "<li>" + i.name + "</li>";
```
Зачем: `StringBuilder` существует, но, видимо, не для нас.

---

## H. Комментарии и оформление

### H1. Комментарий врёт **[2]**
```csharp
// Проверяем, что пользователь активен
if (user.Role == "admin") { ... }
```
Зачем: документация и код живут в разных странах и не созваниваются.

### H2. `TODO` без даты **[2]**
```js
// TODO: вынести в конфиг
const API = "http://10.0.0.14:8080/api";
```
Зачем: маркер вечности. Автор тоже не вернётся.

### H3. Мёртвый код в комментариях **[2]**
```php
// $old = load_from_csv($file);
// $old = array_map('trim', $old);
// TODO: удалить после миграции (2019)
/* $old = load_from_csv($file2); */
```
Зачем: git есть, но комментарии надёжнее.

### H4. Отладка в проде **[1]**
```python
print("!!!")
print(request.data)
print("!!!")
```
Зачем: логирование, но с душой.

### H5. Табы и пробелы **[2]**
```text
\tif (x) {
    \treturn;
 \t}
```
Зачем: отступы как личное мнение. В одном файле — три.

### H6. Выравнивание по колонкам **[3]**
```php
$id       = isset($_GET['id'])     ? (int)$_GET['id']     : 0;
$name     = isset($_GET['name'])   ? $_GET['name']        : '';
$mode     = isset($_GET['mode'])   ? $_GET['mode']        : 'view';
```
Зачем: читается красиво, поддерживается больно.

### H7. Комментарий-эссе **[2]**
```js
/*
 * История изменений:
 * 2013 — сделали
 * 2015 — переделали
 * 2018 — вернули как было
 * 2021 — не трогать, работает
 */
function calc() { return 1; }
```
Зачем: комментарий длиннее функции в 12 раз.

### H8. Комментарий, объясняющий очевидное **[1]**
```python
i = 0  # счётчик
i += 1  # увеличиваем счётчик на 1
```
Зачем: забота, которая не нужна никому.

---

## I. Спецэффекты

### I1. Самодельный `mod` **[3]**
```c
int mod(int a, int b) {
    int r = 0;
    for (int i = 30; i >= 0; i--) {
        r <<= 1;
        if ((a >> i) & 1) r++;
        while (r >= b) r -= b;
    }
    return r;
}
```
Зачем: оператор `%` — для тех, кто не умеет в биты. Классика govnokod #29293.

### I2. Сложение битовыми трюками **[3]**
```php
function sum2($a, $b) { /* XOR + AND + рекурсия, 20 строк */ }
```
Зачем: `+` запрещён код-стайлом.

### I3. JSON через регулярку **[4]**
```js
const id = body.match(/"id"\s*:\s*(\d+)/)[1];
```
Зачем: парсер — это dependency, а dependency — это ответственность.

### I4. HTML через регулярку **[4]**
```python
links = re.findall(r'<a.*?href="(.*?)".*?>(.*?)</a>', html)
```
Зачем: работает на 98% страниц и на 100% страниц заказчика.

### I5. Свой формат даты **[3]**
```js
const stamp = d.getDate() + "" + (d.getMonth() + 1) + "" + d.getFullYear();
// 1112026 — 11 января или 1 ноября?
```
Зачем: сортируется как строка и ломается в марте.

### I6. `eval` для «динамики» **[5] [опасно]**
```js
eval(`result = ${formula}`);
```
Зачем: конфигурируемость за счёт всего остального. Только как демо,
без пользовательского ввода.

### I7. Код с расписанием **[5]**
```python
if datetime.now().weekday() == 1 and datetime.now().hour < 12:
    price *= 1.1   # «так исторически сложилось»
```
Зачем: бизнес-логика, которая знает календарь лучше бухгалтера.

---

## Как комбинировать

- 1–2 приёма из разных групп = шутка.
- 4+ приёма = каша. Читатель не понимает, над чем смеяться.
- **Всегда** оставляй одну нормальную вещь: внятную доменную модель,
  осмысленный SQL, рабочий тест. На её фоне говно видно лучше.