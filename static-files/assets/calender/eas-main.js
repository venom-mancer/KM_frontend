jQuery(document).ready(function($){
// ------------------------------------------------------------------------
   // date1
//  -----------------------------------------------------------------------
	var nina1 = new AMIB.persianCalendar( 'date1', {
						extraInputID: 'edflt',
						extraInputFormat: 'YYYY/MM/DD',
						onchange: function( pdate ){
							if (pdate) {
								$("#month1").prop('disabled', true);
								$("#month1").val(0);
							}
						}
					}
				);
	
	$('#date1').change(function(){
		if (!$('#date1').val()) {
			$("#month1").prop('disabled', false);
		}
	});
// ------------------------------------------------------------------------
//date2
//  -----------------------------------------------------------------------
	var nina2 = new AMIB.persianCalendar( 'date2', {
			extraInputID: 'edflt',
			extraInputFormat: 'YYYY/MM/DD',
			onchange: function( pdate ){
				if (pdate) {
					$("#month2").prop('disabled', true);
					$("#month2").val(0);
				}
			}
		}
	);

	$('#date2').change(function(){
		if (!$('#date2').val()) {
			$("#month2").prop('disabled', false);
		}
    });
    // ------------------------------------------------------------------------
    //date3
    //  -----------------------------------------------------------------------
    var nina3 = new AMIB.persianCalendar('date3', {
        extraInputID: 'edflt',
        extraInputFormat: 'YYYY/MM/DD',
        onchange: function (pdate) {
            if (pdate) {
                $("#month2").prop('disabled', true);
                $("#month2").val(0);
            }
        }
    }
    );

    $('#date3').change(function () {
        if (!$('#date3').val()) {
            $("#month2").prop('disabled', false);
        }
    });
});