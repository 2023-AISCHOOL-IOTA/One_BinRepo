// 회원가입 버튼 누를 시 유효성 검사를 통과하였는지 판단
let isValidUsername = false;
let isValidPassword = false;
let isValidName = false;
let isValidPhone = false;
let checkNum = false;

// 아이디 유효성 검사
// 아이디는 영문+숫자 4~10자리이고 중복된 아이디는 허용하지 않는다.
//[ Dup username ]*/
$("input[name='username']").on("propertychange change keyup paste input", function(){
    let str = $("input[name='username']").val();
    var regExp = /^[0-9a-zA-Z]{4,10}$/;
    if (!regExp.test(str)) {
      $("#dup-username").text("아이디는 영문+숫자 4~10자입니다").css("color", "red");
      isValidUsername = false;
      return;
    }
    $.ajax({
      url:`${path}/users/duplicated/0?str=${str}`,
      type:"GET",
      cache:false,
      success : function(data){
        if (data.success) {
          $("#dup-username").text("사용 가능한 아이디입니다").css("color", "green");
          isValidUsername = true;
        } else {
          $("#dup-username").text(data.msg).css("color", "red");
          isValidUsername = false;
        }
      }
    });
  })

  //비밀번호 유효성 검사
  //비밀번호는 8~16자이고, 비밀번호 확인란과 똑같이 입력해야 한다.
  //[ Dup pass ]*/
$("input[name='re-password']").on("propertychange change keyup paste input", function(){
    let pass1 = $("input[name='password']").val();
    let pass2 = $("input[name='re-password']").val();
    let regExp = /^[a-zA-Z\d`~!@#$%^&*()-_=+]{8,16}$/;
    if (!regExp.test(pass1)) {
      $("#dup-password").text("비밀번호는 8~16자입니다").css("color", "red");
      isValidPassword = false;
      return;
    }
    if (pass1 == pass2) {
      $("#dup-password").text("  비밀번호와 일치합니다");
      $("#dup-password").css("color", "green");
      isValidPassword = true;
    }
    else {
      $("#dup-password").text("  비밀번호와 다릅니다");
      $("#dup-password").css("color", "red");
      isValidPassword = false;
    }
  })
  $("input[name='password']").on("propertychange change keyup paste input", function(){
    let pass1 = $("input[name='password']").val();
    let pass2 = $("input[name='re-password']").val();
    let regExp = /^[a-zA-Z\d`~!@#$%^&*()-_=+]{8,16}$/;
    if (!regExp.test(pass1)) {
      $("#dup-password").text("비밀번호는 8~16자입니다").css("color", "red");
      isValidPassword = false;
      return;
    }
    if (pass1 == pass2) {
      $("#dup-password").text("  비밀번호와 일치합니다");
      $("#dup-password").css("color", "green");
      isValidPassword = true;
    }
    else {
      $("#dup-password").text("  비밀번호와 다릅니다");
      $("#dup-password").css("color", "red");
      isValidPassword = false;
    }
  })

// 전화번호
// 전화번호는 전화번호 양식에 맞는 10~11자리 정수이고 중복을 허용하지 않는다.
//[ Dup phone ]*/
$("input[name='phone']").on("propertychange change keyup paste input", function(){
    let str = $("input[name='phone']").val();
    var regExp = /^01([0|1|6|7|8|9])([0-9]{3,4})([0-9]{4})$/;
    if (!regExp.test(str)) {
      $("#dup-phone").text("올바른 전화번호 11자리를 입력해 주세요").css("color", "red");
      isValidPhone = false;
      return;
    }
    $.ajax({
      url:`${path}/users/duplicated/2?str=${str}`,
      type:"GET",
      cache:false,
      success : function(data){
        if (data.success) {
          $("#dup-phone").text("사용 가능한 번호입니다").css("color", "green");
          isValidPhone = true;
        } else {
          $("#dup-phone").text(data.msg).css("color", "red");
          isValidPhone = false;
        }
      }
    });
  })

  // 전화번호 인증
  // 전화번호 인증을 위해 만든 백 서버 컨트롤러와 서비스, 자바스크립트이다.
 //이 기능을 사용하기 위해서는 백 서버의 build.gradle에 다음 dependency를 추가해야 하고 coolsms 계정이 필요하다. https://coolsms.co.kr/
 const msgModule = require('coolsms-node-sdk').default

// 인증을 위해 발급받은 본인의 API Key를 사용합니다.
// @ResponseBody
// @GetMapping("/phoneCheck")
const apiKey = 'NCSEOYLSEYMZC1Q0'
const apiSecret = 'QKBUAGFWFCRBIBIRMNXR3SAGHWB8NUJA'
const messageService = new msgModule(apiKey, apiSecret);

const params = {
  text: '[쿨에스엠에스 테스트] hello world!', // 문자 내용
  to: '01075588982', // 수신번호 (받는이)
  from: '01075588982' // 발신번호 (보내는이)
}
messageService.sendMany([params]).then(console.log).catch(console.error)
                    