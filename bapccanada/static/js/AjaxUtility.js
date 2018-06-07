export default function doAjaxPost(oData, sUrl, fnSuccess, fnError) {
    $.ajax({
        type: "POST",
        url: sUrl,
        data: oData,
        success: fnSuccess,
        error: fnError,
        dataType: "json",
        success: fnSuccess,
        error: (fnError && typeof fnError === "function") ? fnError : function (error) {
                console.log("Error! " + error);
            }
    });
}