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

    map.addLayer(L.mapbox.styleLayer(geturl()));

}

function geturl(){

    
    var val = document.getElementById("dropdown").value;

    if(val == "Maxtemp")
    {
        style_url='mapbox://styles/kfsand/cl6z3o0g1000v15l6vde2mse2'
        console.log(" setting Maxtemp style")
    }

    if(val == "Gas")
    {
        style_url='mapbox://styles/kfsand/cl6z4fq3t004x15qf00o37936'
        console.log(" setting Gas style")
    }

    if(val == "Nuclear")
    {
        style_url='mapbox://styles/kfsand/cl6z56rit00p014pdr7h1ipi6'
        console.log(" setting Nuclear style")
    }

    if(val == "Hydro")
    {
        style_url='mapbox://styles/kfsand/cl6z3o0g1000v15l6vde2mse2'
        console.log(" setting Hydro style")
    } 

    if(val == "Solar"){
        style_url='mapbox://styles/kfsand/cl6z4pzgb000i14kzusgkll7k'
        console.log(" setting Solar style")
    }
    if(val == "Transformers"){
        style_url='mapbox://styles/kfsand/cl6z4tlro000q14nsvimdc2mc'
        console.log(" setting Transformer style")
    }
    if(val == "OLines"){
        style_url='mapbox://styles/kfsand/cl6z4ysgt000t15nohh32qpn9'
        console.log(" setting OLines style")
    }
    if(val == "Demand"){
        style_url='mapbox://styles/kfsand/cl6z5ave4001e15qmbipd1i03'
        console.log(" setting Demand style")
    }
    return style_url;
}