import doAjaxPost from './AjaxUtility.js';
import getCookie from './CookieUtility.js';

$(document).ready(function () {
    const csrftoken = getCookie('csrftoken');
    const fnDeleteReviewParam = function (oElement, sAction) {
        const sUrl = oElement.id + '/delete';
        const oData = {
            "slug": oElement.id,
            "action": sAction,
            'csrfmiddlewaretoken': csrftoken
        };
        const fnSuccess = function () {
            location.reload()
        }
        return {
            oData: oData,
            sUrl: sUrl,
            fnSuccess: fnSuccess
        };
    };

    const generate_save_button = function () {
        return '<li><a href="javascript:void(0)">save</a></li>'
    }

    const generate_edit_button = function(){
        return '<li><a href="javascript:void(0)">edit</a></li>'
    }

    $('.edit_review').click(function () {
        const id = this.id;
        const card_text = $(`#review-card-${ id } .card-text`);
        console.log(card_text)
        const form = `<div class='form-group'><form><textarea class='form-control'>${card_text[0].innerText}</textarea></form></div>`;
        card_text.replaceWith(form);
        $(this).replaceWith(generate_save_button())
    });

    $('.delete_review').click(function () {

        if (window.confirm(`Are you sure you want to delete review ${this.id}?`)) {
            const oParam = fnDeleteReviewParam(this, "delete");
            doAjaxPost(oParam.oData, oParam.sUrl, oParam.fnSuccess);
            $(this).closest('.review-card').remove();
        }
    });


});