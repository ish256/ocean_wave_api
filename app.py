
# flask modules
from flask import Flask, jsonify, make_response
from flask_restful import Resource, Api, reqparse

import json

# data processing modules
import numpy as np
import pandas as pd

# wave modeling module
import wave_module as wm

# set up a flask app
app = Flask(__name__)

# set up a flask restful api on the flask app
api = Api(app)


# define data to be parsed and validated
parser = reqparse.RequestParser()
parser.add_argument('windspeed', type=float, help='wind speed (m/s)')
parser.add_argument('angle', type=float, help='wind direction (degrees)')

# define an api endpoint class and associated methods
# takes in functionality from flask_restful resource class


class returnWaveMatrixWParam(Resource):

    # define get request associated with path
    def get(self):

        # parse the arguements passed to get call using parser defined earlier
        args = parser.parse_args()
        windSpeed = args['windspeed']
        angle = args['angle']
        # print(windSpeed)
        # print(angle)

        # wind speed constants
        windSpeed = np.array(windSpeed, dtype=float)

        # wind direction vector
        windDirectionVect = [np.cos(np.deg2rad(angle)), np.sin(
            np.deg2rad(angle))]
        windDirectionVect = windDirectionVect/np.linalg.norm(windDirectionVect)

        # will now make the waveVectorField

        spatialExtent = 10  # scene extent in meters
        waveFieldDelta = 2*np.pi/spatialExtent
        N = 128
        k = np.linspace(-N/2, N/2-1, N) * waveFieldDelta

        waveFieldKx, waveFieldKy = np.meshgrid(k, k)

        # make spatial axis
        spatialDelta = spatialExtent/N
        x = np.linspace(-N/2, N/2-1, N) * spatialDelta
        xGrid, yGrid = np.meshgrid(x, x)

        # process data
        spectrum, normWaveField = wm.phillipsSpectrum(
            waveFieldKx, waveFieldKy, windDirectionVect, windSpeed)

        initSpectrum = wm.initWaveSpectrum(spectrum)

        time = 153  # in seconds
        waveAtT = wm.makeWaveFieldAtTimeT(
            initSpectrum, normWaveField, waveFieldDelta, time)

        # add code to smooth wave

        # return as json (approach 2)
        #waveData = pd.DataFrame(waveAtT).to_json(orient='values')
        # waveData = make_response(pd.DataFrame(
        #    waveAtT).to_json(orient="value"))
        # return waveData

        # force it to be real valued
        waveAtT = np.real(waveAtT)

        # reduce precision to 16 bit float
        waveAtT = waveAtT.astype(np.float16)

        result = {'data': waveAtT.tolist(
        ), 'initSpectrum': spectrum.tolist()}
        return jsonify(result)


# add endpoint route
api.add_resource(returnWaveMatrixWParam, '/getwavematrixwparam/')

# if modules name is main (when code run directly) then run
# server at specified address
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
    )
