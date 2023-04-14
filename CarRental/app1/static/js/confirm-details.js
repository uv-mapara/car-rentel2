//$('input:radio[name=Payment]').click(function () {
//    $("input:radio[name=Cash]").prop("checked", false)
//});
//$('input:radio[name=Cash]').click(function () {
//    $("input:radio[name=Payment]").prop("checked", false)
//});


$('#BtnConfirm').click(function (e) {
    var order_id = $('#order_id').val().trim();
    var amount = $('#rent').val().trim();

    var options = {
        "key": "rzp_test_rcgMRmUfjVOdI3",
        // "amount": totalamount*100, 
        "amount": amount,
        "currency": "INR",
        "name": "Car Rentel",
        "description": "Test Transaction",
        "image": "https://example.com/your_logo",
        "order_id": order_id,
        "callback_url": "http://127.0.0.1:8000/success/",        
        "handler": function (response) {
            // alert(response.razorpay_payment_id);
            // alert(response.razorpay_order_id);
            // alert(response.razorpay_signature)
            SaveData();
        },
        "prefill": {
            "name": 'Test',
            "email": 'Test',
            "contact": "9999999999",
        },
        "notes": {
            "address": "Razorpay Corporate Office"
        },
        "theme": {
            "color": "#3399cc"
        }
    };
    var rzp1 = new Razorpay(options);
    rzp1.open();
    e.preventDefault();
});

function SaveData() {    
    var rent = $("#rent").val().trim(); 
    var carname = $("#carname").val().trim(); 
    var days = $("#days").val().trim(); 
    var date = $("#date").val().trim(); 
    var car_dealer = $("#car_dealer").val().trim();     
    var order_id = $("#order_id").val().trim();    
    var payment = $("#payment").val().trim(); 
    var CarID = $("#CarID").val();
    var Days = $("#days").val();
    console.log(Days);

    $.ajax({
        type: 'POST',
        url: '/confirm-details/'+CarID+'/'+Days+'/'+date,
        /*url: '/confirm-details/',*/
        data: {    
            rent: rent,
            carname: carname,
            days: days,
            date: date,
            car_dealer: car_dealer,            
            order_id: order_id,           
            payment: payment,           
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function (resp) {
            alert('Booking Success');
            //if (resp.optstatus == 'Success') {
            //    HideLoader();
            //    window.location.href = "success/";
            //}
        }
    })
}

