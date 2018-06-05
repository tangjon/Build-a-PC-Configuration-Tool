export default function doAjaxPost(oData, sUrl, fnSuccess, fnError) {
    $.ajax({
        type: "POST",
        url: sUrl,
        data: oData,
        dataType: "json",
        success: fnSuccess,
        error: fnError
    });
}