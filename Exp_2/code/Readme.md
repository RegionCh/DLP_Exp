## Report on how Dropout influences ResNet's performance

#### Before Dropout is added

![Train_Acc5](https://github.com/RegionCh/DLP_Exp/blob/master/Exp_2/code/image/Train_acc5.png)

![Train_loss](https://github.com/RegionCh/DLP_Exp/blob/master/Exp_2/code/image/Train_loss.png)

![Val_Acc5](https://github.com/RegionCh/DLP_Exp/blob/master/Exp_2/code/image/Val_acc5.png)

![Val_loss](https://github.com/RegionCh/DLP_Exp/blob/master/Exp_2/code/image/Val_loss.png)

#### Dropout layers is added after BN layers

![Train_Acc5](https://github.com/RegionCh/DLP_Exp/blob/master/Exp_2/code/image/DropoutAfterBN/Train_acc5.png)

![Train_loss](https://github.com/RegionCh/DLP_Exp/blob/master/Exp_2/code/image/DropoutAfterBN/Train_loss.png)

![Val_Acc5](https://github.com/RegionCh/DLP_Exp/blob/master/Exp_2/code/image/DropoutAfterBN/Val_acc5.png)

![Val_loss](https://github.com/RegionCh/DLP_Exp/blob/master/Exp_2/code/image/DropoutAfterBN/Val_loss.png)

#### Dropout layers is added before BN layers

![Train_Acc5](https://github.com/RegionCh/DLP_Exp/blob/master/Exp_2/code/image/DropoutBeforeBN/Train_acc5.png)

![Train_loss](https://github.com/RegionCh/DLP_Exp/blob/master/Exp_2/code/image/DropoutBeforeBN/Train_loss.png)

![Val_Acc5](https://github.com/RegionCh/DLP_Exp/blob/master/Exp_2/code/image/DropoutBeforeBN/Val_acc5.png)

![Val_loss](https://github.com/RegionCh/DLP_Exp/blob/master/Exp_2/code/image/DropoutBeforeBN/Val_loss.png)

#### How to reproduce
You can try different structures by changing dropout layers' position in forward() in resnet.py[Line 92]. If neccessary, you can also pass some parameters through powershell.
The project can be run under python == 3.8.0, pytorch == 1.12.1+cu116, torchvision == 0.13.1

#### Analasis
The graphs shows that when the Dropout layer is not added, serious overfitting will occur soon. As long as the Dropout layer is added, although the training efficiency is reduced, the overfitting of the model can be greatly reduced. Comparing the Dropout location, we can find that the effect of adding it after the BN layer is particularly good. Training a shallow resnet18 on a small-scale dataset can achieve 70% of the top-5 accuracy on the test set. While adding the Dropout layer in front of the BN layer has a good effect on inhibiting overfitting, the final accuracy has not been significantly improved, but the training efficiency has been reduced.

It's natural that serious overfitting occured when Dropout is not added. The data set tiny_imagenet has only 100000 pictures, while resnet has 33161024 parameters, which is much larger than the size of training set.
After Dropout is added, overfitting no longer appears. However, if Dropout is added before BN layer, the result is not good. The reason is that if Dropout is added before BN, when BN layer normalizes neurons on the test data set, the variance calculated by neurons during training will be involved. However, because Dropout discards some neurons during training, the variance calculated by BN in test and training will not be the same, which is called Variance Shifting. As a result, the deviation of Variance Shifting accumulated continuously during the training process, resulting in unsatisfactory results. Adding Dropout after BN can supress Variance Shifting.

#### Conclusion
This experiment mainly explored the influence of interaction between BN layer and Dropout layer on resnet18 training. In the process of theoretical analysis, it is difficult to start. The main reference comes from [1], and some conclusions come from my own thinking and conjecture. In fact, after reading the relevant paper at the beginning, the expectation of the results should be that Dropout is incompatible with BN, resulting in poor training results or even non convergence. Resnet's paper also has related work to support this result. However, my experiment results are not like this. The reason for speculation is that the overfitting of network training is too serious. In contrast, the use of Dropout together with BN brings less side effects of Variance Shifting. In the experiment where the Dropout layer is placed behind the BN layer, because the Dropout layer placed behind all BN layers does not produce Variance Shifting, only the first layer of Dropout will produce Variance Shifting, resulting in less side effects, The training results are better.

#### Reference
[1] Li X ,  Chen S ,  Hu X , et al. Understanding the Disharmony Between Dropout and Batch Normalization by Variance Shift[C]// 2019 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR). IEEE, 2020.      
[2] He K ,  Zhang X ,  Ren S , et al. Identity Mappings in Deep Residual Networks[J]. Springer, Cham, 2016.
