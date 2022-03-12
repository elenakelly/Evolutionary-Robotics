# Evolutionary-Robotics

* Main task: "Create NN & EA for the robot simulator"

• Used mobile robot simulator</br>
• Used ANN as controller </br>
• Used EA to evolve weights of ANN </br>
• Design our own rooms </br>

CODE DIVISION :</br>

(note: robot and EA on benchmark functions were imported from the previous assigments) </br>

Elena Kane i6289291 - </br>
Nikolaos Ntantis i6273751 - </br>
Ioannis Montesantos i6292068 - </br>


ANN:</br>
Used ANN as controller </br>
Used two layers with recurrent nodes</br>
Used feedback to create memory</br>
Play with Dt (depend on time step)</br>
Input: 12 infrared distance sensors (30°distance)</br>
Output: two outputs – each controls speed of one wheel</br>

Fitness criteria:</br>
Collision-free </br>
Fix time for each experiment </br>
Simulate dust, used removed dust as fitness</br>



