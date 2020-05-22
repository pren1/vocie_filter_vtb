import torch
import torch.nn as nn
import traceback

import config
from utils.model_saver import model_saver

def train(embedder, model, optimizer, trainloader, writer, logger, epoch, pt_dir,staring_step):
    try:
        criterion = nn.MSELoss()
        model.train()
        step = staring_step
        for batch_idx, (dvec_mel, target_mag, mixed_mag) in enumerate(trainloader):
            target_mag, mixed_mag = target_mag.cuda(), mixed_mag.cuda()

            dvec_list = list()
            for mel in dvec_mel:
                mel = mel.cuda()
                dvec = embedder(mel)
                dvec_list.append(dvec)
            dvec = torch.stack(dvec_list, dim=0)
            dvec = dvec.detach()
            #mask model
            optimizer.zero_grad()
            mask = model(mixed_mag, dvec)
            output = mixed_mag * mask
            #calculate loss, the paper says it use powerlaw, but we don't do it here

            # output = torch.pow(torch.clamp(output, min=0.0), 0.30)
            # target_mag = torch.pow(torch.clamp(target_mag, min=0.0), 0.30)

            loss = criterion(output, target_mag)
            loss.backward()
            optimizer.step()
            loss = loss.item()
            #log
            step += len(output)
            logger.info('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                epoch, step, len(trainloader.dataset),
                100. * step / len(trainloader), loss))
            if step % config.train.get('summary_interval') == 0:
                writer.log_training(loss, (config.train['train_step_pre_epoch'] * (epoch - 1)) + step)
                logger.info("Wrote Summary at Epoch%d,Step%d" % (epoch, step))
            if step % config.train['ckpt_interval'] == 0 :
                model_saver(model,pt_dir,epoch,step)
                logger.info("Saved Checkpoint at Epoch%d,Step%d" % (epoch, step))
            if step >= config.train['train_step_pre_epoch']: # exit for max step reached
                break
            
    except Exception as e:
        logger.info("Exiting due to exception: %s" % e)
        traceback.print_exc()
