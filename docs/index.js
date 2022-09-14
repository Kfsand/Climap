function hide (){

    //divs to hide
    $("#menu").hide()

    //button
    $("#showUI").show()
    $("#hideUI").hide()
}

function show (){

    $("#menu").show()

    //button
    $("#showUI").hide()
    $("#hideUI").show()

}

function changeMap(){

    var val = document.getElementById("dropdown").value;
        $("#map").attr('data-gc',val)



    L.mapbox.accessToken = 'pk.eyJ1Ijoia2ZzYW5kIiwiYSI6ImNsNTliaHltZzI5dTAzcHQ3b2dhOTFjaTAifQ.vb0ojGjuynKCLg7K2CNMaA';

        var style_url = geturl()
        var map = L.mapbox.map('map')
          .setView([54.729449,-4.519803], 6)
          .addLayer(L.mapbox.styleLayer(style_url));
        show()

}

function geturl(){

    
    var val = document.getElementById("dropdown").value;

    if(val == "Maxtemp")
    alert(" setting Maxtemp style")
    style_url='mapbox://styles/kfsand/cl6z3o0g1000v15l6vde2mse2'

    if(val == "Gas")
    alert(" setting Gas style")
    style_url='mapbox://styles/kfsand/cl6z4fq3t004x15qf00o37936'

    if(val == "Nuclear")
        alert(" setting Nuclear style")
        style_url='mapbox://styles/kfsand/cl6z56rit00p014pdr7h1ipi6'

    if(val == "Hydro")
        alert(" setting Hydro style")
        style_url='mapbox://styles/kfsand/cl6z3o0g1000v15l6vde2mse2'

    if(val == "Solar")
        alert(" setting Solar style")
        style_url='mapbox://styles/kfsand/cl6z4pzgb000i14kzusgkll7k'

    if(val == "Transformers")
        alert(" setting Transformers style")
        style_url='mapbox://styles/kfsand/cl6z4tlro000q14nsvimdc2mc'
    
    if(val == "OLines")
        alert(" setting OLines style")
        style_url='mapbox://styles/kfsand/cl6z5ave4001e15qmbipd1i03'

    if(val == "Demand")
        alert(" setting Demand style")
        style_url='mapbox://styles/kfsand/cl6z5ave4001e15qmbipd1i03'

    return style_url;
}