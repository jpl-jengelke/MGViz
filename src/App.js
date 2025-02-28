import React from 'react'
import essence from './essence/essence'
import $ from 'jquery'
import LandingPage from './essence/LandingPage/LandingPage'

import calls from './pre/calls'

//Start MMGIS
$(document).ready(function () {
    if (window.mmgisglobal.FORCE_CONFIG_PATH) {
        var u = window.location.href.split('?s=')
        if (!u[1]) {
            //Not a shortened URL
            LandingPage.init(null, false, window.mmgisglobal.FORCE_CONFIG_PATH)
        } else {
            calls.api(
                'shortener_expand',
                {
                    short: u[1],
                },
                function (s) {
                    //Set and update the url
                    var url = u[0] + s.body.url
                    window.history.replaceState('', '', url)

                    LandingPage.init(
                        null,
                        false,
                        window.mmgisglobal.FORCE_CONFIG_PATH
                    )
                },
                function (e) {
                    LandingPage.init(
                        null,
                        true,
                        window.mmgisglobal.FORCE_CONFIG_PATH
                    )
                }
            )
        }
    } else {
        calls.api(
            'missions',
            {},
            function (s) {
                continueOn(s.missions)
            },
            function (e) {
                continueOn([])
            }
        )

        function continueOn(missions) {
            var u = window.location.href.split('?s=')
            if (!u[1]) {
                //Not a shortened URL
                LandingPage.init(missions)
            } else {
                calls.api(
                    'shortener_expand',
                    {
                        short: u[1],
                    },
                    function (s) {
                        //Set and update the url
                        var url = u[0] + s.body.url
                        window.history.replaceState('', '', url)
                        LandingPage.init(missions)
                    },
                    function (e) {
                        LandingPage.init(missions, true)
                    }
                )
            }
        }
    }
})

function App() {
    return <div className='App'></div>
}

export default App
