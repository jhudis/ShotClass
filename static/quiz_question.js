function display_ans(ans_true, ans_id, details){
    if(ans_true == true){
        var answer_ops = ``
        for(let i = 0; i < details.options.length; i++){
            let option = details.options[i]
            var html_ops = ``
            if(i == ans_id){
                html_ops = `<button class="btn btn-primary" id="true-btn" data-id='"${i}"'>${option}</button>`
            }
            else{
                html_ops = `<button class="btn btn-primary" id="option-btn" data-id='"${i}"'>${option}</button>`
            }
            answer_ops += html_ops
        }
        $('#clarification').empty()
    }
    else{
        var answer_ops = ``
        for(let i = 0; i < details.options.length; i++){
            let option = details.options[i]
            var html_ops = ``
            if(i == ans_id){
                html_ops = `<button class="btn btn-primary" id="false-btn" data-id='"${i}"'>${option}</button>`
            }
            else{
                html_ops = `<button class="btn btn-primary" id="option-btn" data-id='"${i}"'>${option}</button>`
            }
            answer_ops += html_ops
        }
        $('#clarification').html(`<span id='error-clarification'>${details.clarification}`)
    }
    var html_elem = `
            <div class="row">
                <div>${details.question}</div>
            </div><br>
            <div class="row>
                <div>${details.picture}</div>
            </div><br>
            <div class="row">
                <div>${answer_ops}</div><br>
            </div>
            `
        
    $('#question').html(html_elem)
}

function change_user_stats(question_id, options_id){
    let user_score = {"id": question_id, "answer_id": options_id}
    $.ajax({
        type: "POST",
        url: "change_score",                
        dataType : "json",
        contentType: "application/json; charset=utf-8",
        data : JSON.stringify(user_score),
        success: function(result){
            let all_data = result["data"]
            ans_true = all_data["ans_true"]
            given_ans_id = all_data["ans_id"]
            console.log(ans_true)
            display_ans(ans_true, given_ans_id, details)
        },
        error: function(request, status, error){
            console.log("Error");
            console.log(request)
            console.log(status)
            console.log(error)
        }
    });
}

$(document).ready(function(){
    $('#qstn-title').html(`<div class="row"><b>Question ${id}</div>`)

    var answer_ops = ``
    for(let i = 0; i < details.options.length; i++){
        let option = details.options[i]
        html_ops = `<button class="btn btn-primary" id="option-btn" data-id='"${i}"'>${option}</button>`
        answer_ops += html_ops
    }

    var html_elem = `
        <div class="row">
            <div>${details.question}</div>
        </div><br>
        <div class="row>
            <div>${details.picture}</div>
        </div><br>
        <div class="row">
            <div>${answer_ops}</div><br>
        </div>
        `
    
    $('#question').html(html_elem)

    $('#option-btn').click(function(){
        let index = $(this).data("id")
        options_id = index.replace(/[^0-9]/g,'')
        console.log(options_id)
        change_user_stats(id, options_id)
    });

    var back_id = id - 1
    var forward_id = id + 1

    if(id > 1){
        $('#quiz-btn-back').html(`<a href='/quiz/${back_id}'><button class="btn btn-primary">Back</button></a>`)
    }
    $('#quiz-btn-forward').html(`<a href='/quiz/${forward_id}'><button class="btn btn-primary">Next</button></a>`)
});