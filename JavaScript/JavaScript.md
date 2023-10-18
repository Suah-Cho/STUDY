## 배열

**배열 선언**

```jsx
// 배열 선언
let values = ["빨강", "노랑", "파랑", true, 123];

// 배열의 길이는 배열의 length 속성(propoerty)을 이용해서 확인이 가능
console.log(values.length);
console.log(values["length"]);
```

**배열 요소 접근**

```jsx
// 배열 요소에 접근할 때는 일반적으로 배열의 인덱스를 사용
console.log('첫번째', values[0])
console.log('마지막', values[values.length-1]);
```

**배열 요소에 순차적으로 접근**

```jsx
// 배열 요소에 순차적으로 접근하는 방법
// 방법 1
for ( let i = 0; i < values.length; i ++ ) {
    console.log(values[i])
}

// 방법 2
for (let index in values) {
    console.log(values[index])
}

// 방법 3
for (let color of values) {
    console.log(color)
}

// 방법 4-1
let print = function(color) {
    console.log(color);
}
values.forEach(print)

// 방법 4-2
values.forEach(function(color) {
    console.log(color);
});

// 방법 4-3
values.forEach((color) => {
    console.log(color);
});

// 방법 4-4
values.forEach(color => console.log(color));
```

## 객체

**객체 선언**

키는 중복될 수 없다. 값은 문자열, 숫자, 불리안, 배열, 함수 등 다양하게 가질 수 있다.

```jsx
// 객체 선언
let person = {
    name: "홍길동",
    age :  25,
    inMarried : false,
    'favortie color' : ["red", "yellow"],
    hello : function() {
        return 'hello, Im ' + this.name;
    }
}
```

**객체 속성 참조 및 수정**

```jsx
// 객체 속성을 참조할 때는 객체변수.속성이름 또는 객체변수["속성이름"] 형식을 이용
console.log(person.name);
console.log(person['name'])
console.log(person["favortie color"]);
console.log(person.hello())
// 객체 속성의 값을 변경
person.name = 'gogildong';
console.log(person.name)
```

**객체 속성을 순회하면서 가져오는 방법**

모든 객체 속성을 출력

```jsx
// 객체 속성을 순회하면서 가져오는 방법
console.log('---------------------------')
for (let key in person) {
    console.log(key, ' 속성의 값은 ', person[key]);
    // console.log(key, ' 속성의 값은 ', person.key) 불가
}

// (index):42 Uncaught TypeError: person is not iterable 오류 발생
console.log('---------------------------')
for (let value of person) {
    console.log(value);
}
```

**객체에 속성을 추가 및 삭제**

```jsx
// 빈 객체를 정의
let person = {};
console.log(person);

// 객체에 속성을 추가
person.name = '홍길동';
person.age = 23;
person["favorite colors"] = ['빨강', '파랑'];
console.log(person);
```

**객체가 가지고 있는 모든 속성과 속성의 값을 출력하는 print라는 함수를 객체에 추가**

```jsx
// 객체가 가지고 있는 모든 속성과 속성의 값을 출력하는 print라는 함수를 객체에 추가
person.print = function() {
    for (let key in this) {
        if (key != 'print') {
            console.log(`${key} : ${person[key]}`);
        }
    }
};
person.print();
```

**객체 속성 삭제**

```jsx
// 객체 속성 삭제
delete person.age;
person.print()
```

**객체와 배열을 이용한 데이터 처리**

```jsx
let scores = [];
scores.push({name: '홍길동', korean: 80, math: 90, english: 90});
scores.push({name: '고길동', korean: 90, math: 80, english: 80});
scores.push({name: '신길동', korean: 70, math: 80, english: 70});

console.log(`--------\t------\t------\t------\t------\t------`);
console.log(`학생이름\t국어\t영어\t수학\t합계\t평균`);
console.log(`--------\t------\t------\t------\t------\t------`);

scores.forEach(score => {
    score.sum = function() {
        return this.korean + this.math + this.english;
    };

    score.avg = function() { 
        return Math.round(((this.sum()/3) * 10) / 10);
    };
    console.log(`${score.name}\t${score.korean}\t${score.english}\t${score.math}\t${score.sum()}\t${score.avg()}`)
});
```

### in, with 연산자

**in 연산자**

해당 속성이 객체 존재하는지 여부를 확인

https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Operators/in

```jsx
// in 연산자
console.log("name" in person);
console.log("email" in person);
```

**with 연산자**

사용할 객체를 지정

값을 참조할 때만 사용 가능

https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Template_literals

```jsx
// with 연산자
console.log(`name : ${person.name}`);
console.log(`age : ${person.age}`);
// 반복되는 객체 속성 참조할 때 사용
with(person) {
    console.log(`name : ${name}`);
    console.log(`age : ${age}`);
}
```

## ES6 = ECMAScript 2015

### **단축속성명(shorthand property names)**

```jsx
let name = 'John';
const obj = {
    age : 21,
    name: name,
    getName : function getName() {
        return this.name;
    }
};
console.log(obj);
console.log(obj.getName());

const obj2 = {
    age: 21,
    **name,  // 속성 이름을 생략 <- 속성 이름과 속성값을 가지고 있는 변수 이름이 동일한 경우
    getName()** {  **//            <- 속성 이름과 함수(매소드) 이름이 동일한 경우 function 키워드와 함께 생략**
        return this.name;
    }
};
console.log(obj2);
console.log(obj2.getName());
```

**사용 예 1**

```jsx
// 매개변수를 객체로 반환하는 함수를 정의하는 경우
function retrunObject(age, name) {
    return {age:age, name:name};
}
console.log(retrunObject(20, '홍길동'));

function retrunObject2(age, name) {
    return {age, name};
}
console.log(retrunObject2(20, '홍길동'));

// result
{age: 20, name: '홍길동'}
{age: 20, name: '홍길동'}
```

**사용 예2**

```jsx
// 로그를 출력할 때
const age = 20;
const name = '홍길동';

console.log('age', age);
console.log('name', name);

console.log(`age = ${age}, name = ${name}`);

console.log({age:age, name:name});
console.log({age,name})

// result
age 20
name 홍길동
age = 20, name = 홍길동
{age: 20, name: '홍길동'}
{age: 20, name: '홍길동'}
```

### 계산된 속성명(computed property names)

변수를 이용해서 객체 속성의 키를 만드는 방법

```jsx
// 속성 이름(key)과 속상 값(value)을 전달받아 객체를 반환하는 함수를 정의
function returnObject(key, value) {
  // const obj = {};
  // obj[key] = value;
  // return obj;

  return {[key] : value};
}

console.log(returnObject('name', 'John')); // {name: 'Jogn'}

// 속성 이름이 일련 번호 형태를 가지는 객체를 반환하는 함수
function returnObject2(key, value, no) {
  // const obj = {};
  // obj[key+no] = value;
  // return obj;

  return {[key+no] : value};
}

console.log(returnObject2('name', 'John', 1)); // {name1: 'Jogn'}
console.log(returnObject2('name', 'Machel', 2)); // {name2: 'Machel'}

// result
{name: 'John'}
{name1: 'John'}
{name2: 'Machel'}
```

### **전개 연산자(spread operator)**

```jsx
console.log(Math.max(10,20,1,30,3,2));
console.log(Math.max([10,20,1,30,3,2]));

const numbers = [10,20,1,30,3,2];
console.log(Math.max(numbers));
console.log(Math.max(...numbers));

console.log(numbers);
console.log(...numbers);
```

**사용 예1**

```jsx
let arr1 = [1, 2, 3];
let arr2 = arr1;

console.log(arr1);
console.log(arr2);

arr1[1] = 20;
console.log(arr1);
console.log(arr2);

// 위의 문제(주소가 공유)를 해결하기 위해서는 배열의 주소가 아닌 배열의 값을 복사하는 것이 필요
let arr3 = [1, 2, 3];
let arr4 = [];
for (let i = 0; i < arr3.length; i++ ) {
    arr4[i] = arr3[i];
}
console.log(arr3);
console.log(arr4);

arr3[1] = 20;
console.log(arr3);
console.log(arr4);

// 전개 연산자를 이용해서 복사
let arr5 = [1, 2, 3];
let arr6 = [...arr5];
console.log(arr5);
console.log(arr6);

arr5[1] = 20;
console.log(arr5);
console.log(arr6);

// result
(3) [1, 2, 3]
(3) [1, 2, 3]
(3) [1, 20, 3]
(3) [1, 20, 3]
(3) [1, 2, 3]
(3) [1, 2, 3]
(3) [1, 20, 3]
(3) [1, 2, 3]
(3) [1, 20, 3]
(3) [1, 2, 3]
```

**사용 예 2**

```jsx
let obj1 = {age:23, name:'Hong'};
let obj2 = obj1;
console.log(obj1);
console.log(obj2);

obj1.age = 200;
console.log(obj1);
console.log(obj2);

let obj3 = {age:23, name:'Hong'};
let obj4 = {...obj3};
console.log(obj3);
console.log(obj4);

obj3.age = 200;
console.log(obj3);
console.log(obj4);

// result
{age: 23, name: 'Hong'}
{age: 23, name: 'Hong'}
{age: 200, name: 'Hong'}
{age: 200, name: 'Hong'}
{age: 23, name: 'Hong'}
{age: 23, name: 'Hong'}
{age: 200, name: 'Hong'}
{age: 23, name: 'Hong'}
```

**사용 예 3**

```jsx
// 객체를 복사하는 과정에서 새로운 속성을 추가하거나 속성의 값을 변경하는 경우
let obj1 = {age:23, name: 'Hong'};
obj1.age = 40;
obj1.color = ['red', 'yellow'];
console.log(obj1); //{age: 40, name: 'Hong', color: Array(2)}

// obj1과 동일한 내용을 가지는 obj2를 정의하고, name 속성의 값을 gildon으로 변경
let obj2 = {...obj1, name: 'gildong'};
console.log(obj2); // {age: 40, name: 'gildong', color: Array(2)}

// obj과 동일한 속성을 가지는 obj3를 정의하고, emil 속성을 추가
let obj3 = {...obj1, email: 'test@test.com'};
console.log(obj3) //{age: 40, name: 'Hong', color: Array(2), email: 'test@test.com'}
```

**사용 예 4**

```jsx
// 배열 또는 객체를 결합할 때
// 두 배열을 결합
const arr1 = [1, 2, 3];
const arr2 = [7, 8, 9];

const arr3 = [...arr1, ...arr2];
console.log(arr3); // (6) [1, 2, 3, 7, 8, 9]

const arr4 = [...arr2, ...arr1];
console.log(arr4); // (6) [7, 8, 9, 1, 2, 3]

// 객체를 결합
const obj1 = {age: 21, name: 'hong'};
const obj2 = {hobby: 'soccer', age: 40};

const obj3 = {...obj1, ...obj2};
console.log(obj3) // {age: 40, name: 'hong', hobby: 'soccer'}

const obj4 = {...obj2, ...obj1};
console.log(obj4) // {hobby: 'soccer', age: 21, name: 'hong'}
```

### 배열 비구조화(array destructuring)

배열 데이터(요소)를 변수에 나눠서 할당

```jsx
const arr = [1, 2, 3, 4, 5];
let a = arr[0];
let b = arr[1];
console.log(a, b); // 1 2

// c, d, e, f 변수에 arr 배열에 첫번째 인덱스부터 차례로 할당
let [c, d, e, f] = arr;
console.log(c, d, e, f); // 1 2 3 4
```

**사용 예**

```jsx
// 두 변수의 값을 교환
let x = 10;
let y = 20;
console.log(x, y); // 10 20

[x, y] = [y, x]
// 비구조화 = 배열
console.log(x, y) // 20 10
```

```jsx
{
    // 배열의 크기 보다 변수의 개수가 많은 경우, 기본값 설정이 가능
    const arr = [1,2];
    let [a, b, c] = arr;
    console.log(a, b, c)  // 1 2 undefined

    let [x, y = 20 , z = 30] = arr;
    console.log(x, y, z); // 1 2 30
}

{
    // 배열의 일부값을 변수에 할당할 경우, 할당하지 않을 자리는 비워둠
    const arr = [1, 2, 3];
    let a = 10, b = 20, c = 30;
    console.log(a, b, c); // 10 20 30

    // 변수 a에 1, 변수 c에 3을 재할당하고 변수 b는 20을 그대로 유지하는 경우
    [ a, , c] = arr;
    console.log(a, b, c); // 1 20 3
}

{
    // 배열의 값을 할당하고 남은 나머지를 새로운 배열로 만드는 경우
    const arr = [1, 2, 3, 4, 5];

    // arr 배열의 첫번째 값을 fisrt 변수에 넣고, 나머지 값을 rest라는 이름의 배열에 추가
    const [first, ...rest] = arr;
    console.log(first); // 1
    console.log(rest); // (4) [2, 3, 4, 5]
}
```

**객체 비구조화(object destructuring)**

```jsx
// 객체 비구조화를 할 때는 객체의 속성명(key)이 중요
const obj1 = { age: 21, name: 'mike'}
const obj2 = {age: 40, name: 'john'}

{
    
// obj1의 age와 name 속성의 값을 age와 name 변수에 할당
    const {age, name} = obj1;
    console.log(age, name); // 21 'mike'

    const {age2, name2} = obj1;
    console.log(age2, name2); // undefined undefined

}

{
    
// 객체 비구조화를 통해 가져온 값을 새로운 변수 이름으로 사용할 경우 => 별칭 부여
    const { age : ageNew, name : nameNew } = obj1;
    console.log(ageNew, nameNew); // 21 'mike'

}

{
    
// 객체에 존재하지 않는 요소를 변수에 할당할 때 적용할 기본값 설정도 가능
    const { age, name: nameNew, email = 'test@test.com' } = obj1;
    console.log(age, nameNew, email); // 21 'mike' 'test@test.com'
}

{
    
// 객체 비구조화와 새 객체의 일부 속성을 변수에 저장하고, 나머지를 새로운 객체로 저장
    const obj3 = {age:32, name:'John', grade:'C'};
    // obj3의 age 속성의 값을 johnAge변수에 할당하고, 나머지를 rest이름의 객체에 할당
    const {age:johnAge, ...rest} = obj3;
    console.log(johnAge, rest); // 32 {name: 'John', grade: 'C'}
}
```

**화살표 함수**

익명 함수 표현식을 이용한 함수 정의

```jsx
let add = function(a, b) { return a + b; };
```

화살표 함수

1. funcion키워드를 제거하고, 함수 파라미터의 본문 사이에 ⇒ 를 추가

```jsx
let add2 = ( a, b ) => { return a + b; };
```

1. 화살표 함수 본문의 중괄호를 제거하면 화살표 오른쪽의 결과를 반환

```jsx
let add3 = ( a, b ) => a + b;
```

1. 파라미터가 하나이면 파라미터를 감싸고 있는 소괄호도 생략이 가능

```jsx
let add4 = a => a + 4;
console.log(add4(10)); // 14
```

1. 객체를 반환하는 경우에는 소괄호를 감싸야 함

```
let add5 = (a, b) => {return {result : a + b}};
console.log(add5(10, 20)); // {result: 30}

let add6 = (a, b) => ( { result : a + b} );
console.log(add6(10, 20)); // {result: 30}
```

### map() 함수

**source배열의 값을 두 배수한 결과 배열(twoTimes)을 만들어서 출력하시오**

```jsx
const source = [1, 4, 9, 16];
const twoTimes = source.map(value => value * 2);
console.log(twoTimes);  // (4) [2, 8, 18, 32]
```

```jsx
const f1 = value => value * 2;
const f2 = value => value * 10;
const twoTimes = source.map(f1).map(f2);
console.log(twoTimes); // (4) [20, 80, 180, 320]
```

### filter() 함수

```jsx
const words = [ 'spray', 'limit', 'elite', 'destruction', 'present', 'exuberant' ];

// 여섯 글자 이상의 단어만 추출
{
    const newWords = words.filter(word => word.length > 6);
    console.log(newWords); // (3) ['destruction', 'present', 'exuberant']
}

```

```jsx
const numbers = [1, 3, 4, 6, 11, 14];
// 짝수를 추출해서 10배수한 결과를 출력
{
    console.log(numbers.filter(num => num % 2 === 0).map(num => num * 10)); // (3) [40, 60, 140]
}
```

### reduce() 함수

```jsx
const numbers = [1, 2, 3, 4, 5];
// 배열 데이터의 합계
{
    let sum = numbers.reduce((previous, current) => previous + current);
    console.log(sum); // 15
}
```

```jsx
// numbers 배열의 각 항목의 값에 13을 곱한 결과 중 짝수의 합을 구하시오.
{
    console.log(numbers.map(num => num * 13).filter(num => num % 2 === 0 ).reduce((previous, current) => previous + current)) // 78
}
```

```jsx
let scores = [];
scores[0] = {name: '홍길동', korean: 80, math: 90, english: 90};
scores.push({name: '고길동', korean: 90, math: 80, english: 80});
scores.push({name: '신길동', korean: 70, math: 80, english: 70});
console.log(scores);

// 방법 1
console.log('국어 점수 총합' , scores.map(s => s.korean).reduce((p, c) => p + c));
console.log('수학 점수 총합' , scores.map(s => s.math).reduce((p, c) => p + c));
console.log('영어 점수 총합' , scores.map(s => s.english).reduce((p, c) => p + c));

// 방법 2
const f = x => scores.map(x).reduce((p, c) => p + c);

console.log('국어 점수 총합' , f(s => s.korean));
console.log('수학 점수 총합' , f(s => s.math));
console.log('영어 점수 총합' , f(s => s.english));
```

### axios를 이용한 외부 데이터를 연동

https://restcountries.com/v3.1/all?fields=name,flags

**데이터 구조**

```json
{
	"flags": {
	"png": "https://flagcdn.com/w320/kr.png",
	"svg": "https://flagcdn.com/kr.svg",
	"alt": "The flag of South Korea has a white field, at the center of which is a red and blue Taegeuk circle surrounded by four black trigrams, one in each corner."
},
"name": {
	"common": "South Korea",
	"official": "Republic of Korea",
	"nativeName": {
		"kor": {
			"official": "대한민국",
			"common": "한국"
			}
		}
	}
}
```

```jsx
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
   
    <!-- 실행에 필요한 자바스크립트 라이브러리를 추가 -->
    <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
    <script src="https://code.jquery.com/jquery-3.7.0.min.js" integrity="sha256-2Pmvv0kuTBOenSvLm6bvfBSSHrUJ+3A7x6P5Ebd07/g=" crossorigin="anonymous"></script>
</head>
<body>
    <ul>
    </ul>
    <script>
       // axios를 이용해서 국가 및 국기 데이터를 가져옴
       axios.get('https://restcountries.com/v3.1/all?fields=name,flags')
            .then(res => {
                console.log(res.data);

                res.data.forEach(nf => {
                    // console.log(nf.flags.png, nf.name.common);
                    const {flags, name} = nf;
                    const li = `
                    <li>
                        <img src="${flags.png}" alt="${flags.alt}"/>
                        <p>${name.common}${name.official}</p>
                     </li>
                     `;
                     $('ul').append(li);
                });
            })
            .catch(err => console.log(err));
    </script>
</body>
</html>
```