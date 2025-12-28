# usage
```
from utils.auth import jwt_required

 @blueprint.route('/protected', methods=['GET'])
@jwt_required
 def protected_route():
 return jsonify({'message': 'This is protected'})