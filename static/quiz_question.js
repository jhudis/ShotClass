function display_ans(ans_true, ans, details, button){
    if(ans_true == false){
        $(button).css('background-color', 'red')

        $('#clarification').html(`<span id='error-clarification'>${details.clarification}`)
    }
    else{
        $(button).css('background-color', 'green');
    }
    var html_elem = `
            <div class="row">
                <div>${details.question}</div>
            </div><br>
            <div class="row">
                <img src='${details.picture}'></div>
            </div><br>
            <div class="row">
                ${answer_ops}<br>
            </div>
            `
        
    $('#question').html(html_elem)
}

function change_user_stats(id, value, button){
    let user_score = {"id": id, "answer": value}
    $.ajax({
        type: "POST",
        url: "change_score",                
        dataType : "json",
        contentType: "application/json; charset=utf-8",
        data : JSON.stringify(user_score),
        success: function(result){
            let all_data = result["data"]
            ans_true = all_data["ans_true"]
            given_ans = all_data["ans"]
            console.log(ans_true)
            display_ans(ans_true, given_ans, details, button)
        },
        error: function(request, status, error){
            console.log("Error");
            console.log(request)
            console.log(status)
            console.log(error)
        }
    });
}

function check_ans(){
    $('#ans-fs').click(function(){
        var button = '#ans-fs'
        var value = $(this).text()
        console.log(value);
        change_user_stats(id, value, button)
    });

    $('#ans-mfs').click(function(){
        var button = '#ans-mfs'
        var value = $(this).text()
        console.log(value);
        change_user_stats(id, value, button)
    });

    $('#ans-cs').click(function(){
        var button = '#ans-cs'
        var value = $(this).text()
        console.log(value);
        change_user_stats(id, value, button)
    });

    $('#ans-ms').click(function(){
        var button = '#ans-ms'
        var value = $(this).text()
        console.log(value);
        change_user_stats(id, value, button)
    });

    $('#ans-mcu').click(function(){
        var button = '#ans-mcu'
        var value = $(this).text()
        console.log(value);
        change_user_stats(id, value, button)
    });

    $('#ans-cu').click(function(){
        var button = '#ans-cu'
        var value = $(this).text()
        console.log(value);
        change_user_stats(id, value, button)
    });

    $('#ans-ecu').click(function(){
        var button = '#ans-ecu'
        var value = $(this).text()
        console.log(value);
        change_user_stats(id, value, button)
    });
}

$(document).ready(function(){
    $('#qstn-title').html(`<div id='qstn-title' class="row"><b>Question ${id}</div>`)

    var html_elem = `
        <div class="row">
            <div id='qstn-qstn'>${details.question}</div>
        </div><br>
        <div class="row" id='img-row'>
            <img id='quiz-img' src='${details.picture}'>
        </div><br>
        `
    
    $('#question').html(html_elem)

    check_ans()

    var back_id = id - 1
    var forward_id = id + 1

    if(id > 1){
        $('#quiz-btn-back').html(`<a href='/quiz/${back_id}'><button class="btn">Back</button></a>`)
    }
    $('#quiz-btn-forward').html(`<a href='/quiz/${forward_id}'><button class="btn">Next</button></a>`)
});