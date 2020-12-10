
import logging
from app.logic.solver import *

resolvers = {
    'Query': {
        'solve': lambda value, info, **args: solve(args['problem']),
        'initLPProblem': lambda value, info, **args: {
            'id': args['probID'],
            'desc': args.get('probDesc', None),
            'objective': {
                'id': args['probID'],
                'expr': {
                    'id': args['probID'],
                    'expr': []
                },
                'isMaximize': True,
            },
            'constraints': [],
        },
        'setObjective': lambda value, info, **args: setObjective(args['problem'], args['objective']),
        'binaryVariable': lambda value, info, **args: {
            'id': args['varID'],
            'desc': args.get('desc', None),
            'isInteger': True,
            'isBinary': True,
            'lowerBound': 0.0,
            'upperBound': 1.0,
        },
        'addConstraint': lambda value, info, **args: addConstraint(args['problem'], args['constraint']),
        'addConstraints': lambda value, info, **args: addConstraints(args['problem'], args['constraints']),
        'createLpExpression': lambda value, info, **args: {
            'id': id(),
            'desc': args.get('desc', None),
            'expr': [{
                'id': id(),
                'lpVar': args['variable'],
                'coef': args['coef']
            }]
        },
        'addExpressions': lambda value, info, **args: {
            'id': args['toThis']['id'],
            'desc': args['toThis']['desc'],
            'expr': args['toThis']['expr'] + args['addThis']['expr']
        },
        'createGEConstraint': lambda value, info, **args: {
            'id': id(),
            'desc': args.get('desc', None),
            'expr': args['expr'],
            'type': '>=',
            'value': args['constraintValue']
        },
        'createLEConstraint': lambda value, info, **args: {
            'id': id(),
            'desc': args.get('desc', None),
            'expr': args['expr'],
            'type': '<=',
            'value': args['constraintValue']
        },
        'createEQConstraint': lambda value, info, **args: {
            'id': id(),
            'desc': args.get('desc', None),
            'expr': args['expr'],
            'type': '=',
            'value': args['constraintValue']
        },
    },
    'Mutation': {
    },
    'Object': {
    },
    'Scalar': {
    },
}

