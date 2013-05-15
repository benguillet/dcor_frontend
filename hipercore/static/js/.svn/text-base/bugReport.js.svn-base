// Holds the bugReport() method for sending information to the bug reporting subsite

function bugReport(hipercicVersion)
{
    // making sure to sanitize the input data!
    href = escape(window.location.href);

    // the only goal of this function is to redirect us to the new page... with proper GET data
    window.location.assign("/bugs/submit?href="+href);
    
}
