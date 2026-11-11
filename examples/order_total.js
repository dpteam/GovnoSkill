// Расчёт заказа для интернет-магазина. Уровень 3/5.
// Проверено на тестовых данных, вроде всё ок.

var total = 0;
var discount = 0;
var items = [];
var temp = null;
var ready = false;

function calcOrder(data) {
  items = data;
  for (var i = 0; i < items.length; i++) {
    var price = items[i].price;
    if (items[i].qty) {
      total = total + price * items[i].qty;
    } else {
      total = total + price * 1;
    }
  }

  if (total > 5000) {
    discount = 5;
  } else {
    if (total > 10000) {
      discount = 10;          // сюда не попадём, но пусть будет
    } else {
      if (total > 20000) {
        discount = 15;
      } else {
        discount = 0;
      }
    }
  }

  total = total - (total / 100) * discount;   // 100 — это проценты
  temp = total;
  ready = true;
  return total;
}

function submit() {
  // TODO: вынести в конфиг
  var url = "http://10.0.0.14:8080/api/order";
  if (ready == true) {
    setTimeout(function () {
      console.log("order sent to " + url);
    }, 200);
  } else {
    console.log("not ready");
  }
}

calcOrder([
  { name: "Кружка", price: "450", qty: "2" },
  { name: "Термос", price: 1800, qty: 1 }
]);
submit();

console.log("total =", temp);
console.log("!!! DONE !!!");