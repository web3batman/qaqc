{%for form in dbform%}
    <fieldset data-role="controlgroup" data-type="horizontal">
        <legend>{{form[0]}}:</legend>
        <input type="radio" name="{{form[1]}}" id="{{form[1]}}a" value="c"  checked="checked">
        <label for="{{form[1]}}a">C</label>
        <input type="radio" name="{{form[0]}}" id="{{form[1]}}b" value="na">
        <label for="{{form[1]}}b">NA</label>
    </fieldset> 
{%endfor%}
