export default function doAjaxPost(oData, sUrl, fnSuccess, fnError) {
    $.ajax({
        type: "POST",
        url: sUrl,
        data: oData,
        success: fnSuccess,
        error: fnError
    });
}