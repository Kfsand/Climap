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

    if(val == "Maxtemp1")
    {
        style_url='mapbox://styles/kfsand/cl6z3o0g1000v15l6vde2mse2'
        console.log(" setting Maxtemp style")
    }

    if(val == "Gas1")
    {
        style_url='mapbox://styles/kfsand/cl6z4fq3t004x15qf00o37936'
        console.log(" setting Gas style")
    }

    if(val == "Nuclear1")
    {
        style_url='mapbox://styles/kfsand/cl6z56rit00p014pdr7h1ipi6'
        console.log(" setting Nuclear style")
    }

    if(val == "Solar1"){
        style_url='mapbox://styles/kfsand/cl6z4pzgb000i14kzusgkll7k'
        console.log(" setting Solar style")
    }
    if(val == "Transformers1"){
        style_url='mapbox://styles/kfsand/cl6z4tlro000q14nsvimdc2mc'
        console.log(" setting Transformer style")
    }
    if(val == "OLines1"){
        style_url='mapbox://styles/kfsand/cl6z4ysgt000t15nohh32qpn9'
        console.log(" setting OLines style")
    }
    if(val == "Demand1"){
        style_url='mapbox://styles/kfsand/cl6z5ave4001e15qmbipd1i03'
        console.log(" setting Demand style")
    }
    if(val == "Maxtemp2")
    {
        style_url='mapbox://styles/kfsand/cl6ywwt37003r14upwdh1pwn2'
        console.log(" setting Maxtemp style")
    }

    if(val == "Gas2")
    {
        style_url='mapbox://styles/kfsand/cl6wk0b8b001314o2ib5f0pz4'
        console.log(" setting Gas style")
    }

    if(val == "Nuclear2")
    {
        style_url='mapbox://styles/kfsand/cl6wl0sg9001614qlxu93kity'
        console.log(" setting Nuclear style")
    }

    if(val == "Solar2"){
        style_url='mapbox://styles/kfsand/cl6xbp7x4001114pq9ss8np48'
        console.log(" setting Solar style")
    }
    if(val == "Transformers2"){
        style_url='mapbox://styles/kfsand/cl6xbwzdv001k14qloi1oui41'
        console.log(" setting Transformer style")
    }
    if(val == "OLines2"){
        style_url='mapbox://styles/kfsand/cl6xccwb5007r14p4cs9o116z'
        console.log(" setting OLines style")
    }
    if(val == "Demand2"){
        style_url='mapbox://styles/kfsand/cl6xcq6iy002a14muvmkqllq9'
        console.log(" setting Demand style")
    }
    return style_url;
}